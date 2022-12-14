from fastapi import BackgroundTasks, FastAPI
from time import time
from typing import Union
import asyncio
import httpx
import joblib
import pandas as pd
import random


app = FastAPI()

# Hello test
@app.get('/hello')
def read_root():
    return {'Hello': 'World!'}


model = joblib.load('model.joblib')

X_train = joblib.load('xtrain.joblib')
X_test = joblib.load('xtest.joblib')
y_test = joblib.load('ytest.joblib')
new_data = pd.DataFrame(columns=['glucose', 'bmi', 'age'])
y_new_data = pd.DataFrame(columns=['Outcome'])

# Background task
async def write_new_data(glucose: int, bmi: float, age: int, pred: int):
    global new_data
    global y_new_data
    global model
    new_data.loc[len(new_data)] = [glucose, bmi, age]
    y_new_data.loc[len(y_new_data)] = [random.randint(0, 1)]
    # Retrain model 
    if len(new_data) > 400:
        print("Score before : ", model.score(X_test, y_test))
        model.fit(new_data, y_new_data['Outcome'])
        print("Model trained with new data ! New score : ", model.score(X_test, y_test))
        # Clean the new_datas
        new_data = new_data.iloc[0:0]
        y_new_data = y_new_data.iloc[0:0]

# Predictions
@app.post('/predict')
def predict_model(glucose: int, bmi: float, age: int, background_tasks: BackgroundTasks):
    # background_tasks.add_task(write_new_data, glucose, bmi, age)
    # background_tasks.add_task(get_auc, X_train, new_data) 
    pred = model.predict(pd.DataFrame({'glucose': [glucose], 'bmi': [bmi], 'age': [age]}))
    background_tasks.add_task(write_new_data, glucose, bmi, age, int(pred[0]))
    return {'prediction': int(pred[0])}

async def predict_request(client):
    data = {'glucose': int(random.gauss(105, 30)), 'bmi': random.gauss(33, 7), 'age': int(random.uniform(20, 70))}
    response = await client.post('http://localhost:8000/predict', params=data)
    return response.text

async def predict_task(n: int) -> None:
    async with httpx.AsyncClient() as client:
        tasks = [predict_request(client) for i in range(n)]
        await asyncio.gather(*tasks)
        #print(result)

@app.get('/predict/{n}')
async def predict_n_requests(n: int):
    start = time()
    await predict_task(n)
    return {'time': time() - start}


# Get new data
@app.get('/new_data')
def get_new_data():
    return {'glucose': new_data.glucose, 'bmi': new_data.bmi, 'age': new_data.age}