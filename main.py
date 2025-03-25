from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Connect to Redis

redis_conn = get_redis_connection(
    host="redis-12894.c1.us-east1-2.gce.redns.redis-cloud.com",
    port=12894,
    password="oUDjGzd2h2ljd6FyVIMdyvTp4gE3celk",
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis_conn

@app.get("/orders/{id}")
async def read(id: str):
    return Order.get(id)

@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    req = requests.get('http://localhost:8002/products/%s' % body['id'])
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee= 0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )

    order.save()
    background_tasks.add_task(order_complete, order)

    return order

def order_complete(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis_conn.xadd('order_completed', order.model_dump())