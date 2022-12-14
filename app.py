from fastapi import BackgroundTasks, FastAPI
from fastapi_utils.tasks import repeat_every
from time import time
from typing import Union
import asyncio
import httpx
import joblib
import pandas as pd
import random

def create_new_data(n: int):
    data = pd.DataFrame(columns=['glucose', 'bmi', 'age', 'Outcome'])
    for i in range(n):
        diabetic = random.randint(0, 1)
        if diabetic == 1:
            data.loc[len(data)] = [random.randint(110, 200), random.randint(30, 50), random.randint(40, 70), 1]
        else:
            data.loc[len(data)] = [random.randint(60, 120), random.randint(17, 33), random.randint(20, 50), 0]
    X = data[['glucose', 'bmi', 'age']]
    y = data[['Outcome']]

    return X, y


app = FastAPI()

# Hello test
@app.get('/hello')
def read_root():
    return {'Hello': 'World!'}


model = joblib.load('model.joblib')

X_test = joblib.load('xtest.joblib')
y_test = joblib.load('ytest.joblib')

new_data = pd.DataFrame(columns=['glucose', 'bmi', 'age'])
y_new_data = pd.DataFrame(columns=['Outcome'])


# Background task
async def write_new_data(glucose: int, bmi: float, age: int, pred: int):
    new_data.loc[len(new_data)] = [glucose, bmi, age]
    y_new_data.loc[len(y_new_data)] = [pred]


@app.on_event("startup")
@repeat_every(seconds=30, raise_exceptions=True)
def retrain():
    global new_data
    global y_new_data
    old_score = model.score(X_test, y_test)
    X_retrain, y_retrain = create_new_data(500)
    X_retrain = pd.concat([X_retrain, new_data], ignore_index=True)
    y_retrain = pd.concat([y_retrain['Outcome'], y_new_data['Outcome']], ignore_index=True)
    model.fit(X_retrain, y_retrain)
    print(f'retraining -> old score: {old_score} / new score: {model.score(X_test, y_test)}')
    if len(new_data) > 400:
        new_data = new_data.iloc[0:0]
        y_new_data = y_new_data.iloc[0:0]


# Predictions
@app.post('/predict')
def predict_model(glucose: int, bmi: float, age: int, background_tasks: BackgroundTasks):
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

@app.get('/predict/{n}')
async def predict_n_requests(n: int):
    start = time()
    await predict_task(n)
    return {'time': time() - start}


# Get new data
@app.get('/new_data')
def get_new_data():
    return {'glucose': new_data.glucose, 'bmi': new_data.bmi, 'age': new_data.age}