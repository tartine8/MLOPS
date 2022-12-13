from fastapi import FastAPI
from typing import Union
import fasttext

model = fasttext.load_model('imdb_model.bin')

app = FastAPI()

@app.get('/hello')
def read_root():
    return {'Hello': 'World!'}

@app.post('/predict')
def predict_model(text: str):
    pred = model.predict(text)
    return {'prediction': pred[0][0], 'confidence': pred[1][0]}