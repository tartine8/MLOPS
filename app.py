#from eurybia import SmartDrift
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
new_data = pd.DataFrame(columns=['glucose', 'bmi', 'age'])

# Background task
async def write_new_data(glucose: int, bmi: float, age: int):
    new_data.loc[len(new_data)] = [glucose, bmi, age]

# Drift
#def get_auc(X_train, X_prod):
#    drift = SmartDrift(df_current=X_prod, df_baseline=X_train, deployed_model=model)
#    drift.compile()
    # if drift.auc > 0.7:
    #     print("THE MODEL MIGHT DRIFT")
    # else:
    #     print("THE MODEL DOES NOT DRIFT")


# Predictions
@app.post('/predict')
def predict_model(glucose: int, bmi: float, age: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_new_data, glucose, bmi, age)
    #background_tasks.add_task(get_auc, X_train, new_data) 
    pred = model.predict(pd.DataFrame({'glucose': [glucose], 'bmi': [bmi], 'age': [age]}))
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