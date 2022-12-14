from eurybia import SmartDrift
from fastapi import BackgroundTasks, FastAPI
from time import time
from typing import Union
import asyncio
import fasttext
import httpx
import pandas as pd
import pickle


model = fasttext.load_model('imdb_model.bin')

new_data = pd.DataFrame({'text': []})
with open('new_data.pkl', 'wb') as file:
    pickle.dump(new_data, file)

app = FastAPI()

# Background task
async def write_new_data(text: str):
    with open("new_data.pkl", mode="rb") as file:
        data = pickle.load(file)
    data.loc[len(data)] = [text]
    with open("new_data.pkl", mode="wb") as file:
        pickle.dump(data, file)


# Hello test
@app.get('/hello')
def read_root():
    return {'Hello': 'World!'}

async def hello_request(client):
    response = await client.get('http://localhost:8000/hello')
    return response.text

async def hello_task(n: int) -> None:
    async with httpx.AsyncClient() as client:
        tasks = [hello_request(client) for i in range(n)]
        result = await asyncio.gather(*tasks)
        print(result)

@app.get('/hello100')
async def print_100_hello():
    start = time()
    await hello_task(100)
    return {'time': time() - start}


# Get new data
@app.get('/new_data')
def get_new_data():
    with open("new_data.pkl", mode="rb") as file:
        data = pickle.load(file)
    return {'data': data.text}


# Drift
async def get_auc(X_train, X_prod):
    drift = SmartDrift(df_current=X_prod, df_baseline=X_train, deployed_model=model)
    drift.compile(full_validation=True)
    if drift.auc > 0.7:
        print("THE MODEL MIGHT DRIFT")
    else:
        print("THE MODEL DOES NOT DRIFT")


# Predictions
@app.post('/predict')
def predict_model(text: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_new_data, text)
    background_tasks.add_task(get_auc, 'new_data.pkl', 'train.txt')
    #new_data.loc[len(new_data)] = [text]
    pred = model.predict(text)
    return {'prediction': pred[0][0], 'confidence': pred[1][0]}

async def predict_request(client):
    data = {'text': 'omg this movie was incredible'}
    response = await client.post('http://localhost:8000/predict', params=data)
    return response.text

async def predict_task(n: int) -> None:
    async with httpx.AsyncClient() as client:
        tasks = [predict_request(client) for i in range(n)]
        result = await asyncio.gather(*tasks)
        #print(result)

@app.get('/predict/{n}')
async def predict_n_requests(n: int):
    start = time()
    await predict_task(n)
    return {'time': time() - start}