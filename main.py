#####
# Filename: main.py
# Created Date: Saturday, April 29th 2023, 8:44:33 pm
# Author: Alejandro Gómez Jiménez (xandross389@gmail.com)
# -----
# Copyright (c) 2023 - MIT License
# -----
# Last Modified: Sun Apr 30 2023
# Modified By: Alejandro Gómez Jiménez
#####

from fastapi import FastAPI, Response
from typing import List, Dict
from pydantic import BaseModel

ALLOWED_CRITERIONS = ["completed", "pending", "canceled", "all"]
ALLOWED_ORDER_STATUS = ALLOWED_CRITERIONS[:-1]
class Order(BaseModel):
    id: int
    item: str
    quantity: int
    # price:  Annotated[float, Body(gt=0)] # pydantic validation method
    price: float
    status: str
class SolutionRequest(BaseModel):
    orders: List[Order]
    criterion: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/solution")
async def solution(request: SolutionRequest, response: Response):
    """
    {
        "orders": [
            {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
            {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
            {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
            {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
        ],
        "criterion": "completed"
    }
    """
    if request.criterion not in ALLOWED_CRITERIONS:
        return {"message": f"unknown criterion {request.criterion}"}

    for order in request.orders:
        if order.price < 0:
            response.status_code = 400
            return {"message": f"invalid price {order.price} for order {order.id}"}
        if order.status not in ALLOWED_ORDER_STATUS:
            response.status_code = 400
            return {"message": f"invalid status {order.status} for order {order.id}"}

    try:
        result = 0
        orders_dict_list = []
        for order in request.orders:
            orders_dict_list.append(dict((x, y) for x, y in order))
        result = process_orders(orders_dict_list, request.criterion)
    except:
        response.status_code = 500
        return {"message": f"error processing orders list"}

    response.status_code = 200
    return {"solution": result}

def process_orders(orders: List[Dict], criterion: str) -> float:
    total = 0
    for order in orders:
        if order["status"] == criterion or criterion == "all":
            total += order["price"] * order["quantity"]
    return round(total, 2)
