from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import fasttext

model = fasttext.load_model('imdb_model.bin')

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get('/hello')
def read_root():
    return {'Hello': 'Paul!'}

@app.get('/item/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}

@app.put('/item/{item_id}')
def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}

@app.post('/predict')
def predict_model(text: str):
    pred = model.predict(text)
    return {'prediction': pred[0][0], 'confidence': pred[1][0]}