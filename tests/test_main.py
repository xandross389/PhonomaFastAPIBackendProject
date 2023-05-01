#####
# Filename: test_main.py
# Created Date: Saturday, April 29th 2023, 9:55:06 pm
# Author: Alejandro Gómez Jiménez (xandross389@gmail.com)
# -----
# Copyright (c) 2023 - MIT License
# -----
# Last Modified: Sun Apr 30 2023
# Modified By: Alejandro Gómez Jiménez
#####

import main
from fastapi.testclient import TestClient

orders = [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 4.44, "status": "canceled"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 2.22, "status": "pending"}
    ]

def test_process_orders():
    assert main.process_orders(orders, "completed") == 1299.69
    assert main.process_orders(orders, "pending") == 1004.34
    assert main.process_orders(orders, "canceled") == 117.72
    assert main.process_orders(orders, "all") == 2421.75
    assert main.process_orders(orders, "invalid_status") == 0

#
# TESTS CASES FOR REST API
#

client = TestClient(main.app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_process_invalid_criterion():
    """ test process invalid_criterion """
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": orders, 
            "criterion": "invalid_criterion"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "unknown criterion invalid_criterion"
    }

def test_process_invalid_order_status():    
    """ test invalid order status """    
    invalid_orders = orders.copy()
    invalid_orders.append({"id": 20, "item": "Laptop", "quantity": 1, "price": 1.0, "status": "invalid_status"})
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": invalid_orders, 
            "criterion": "completed"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "message": "invalid status invalid_status for order 20"
    }

def test_process_invalid_order_price():    
    """ test invalid order price """
    invalid_orders = orders.copy()
    invalid_orders.append({"id": 10, "item": "Laptop", "quantity": 1, "price": -1.0, "status": "completed"})
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": invalid_orders, 
            "criterion": "completed"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "message": "invalid price -1.0 for order 10"
    }


def test_process_correct_orders():    
    """ test process all """
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": orders, 
            "criterion": "all"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "solution": 2421.75
    }
    """ test process completed """
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": orders, 
            "criterion": "completed"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "solution": 1299.69
    }
    """ test process canceled """
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": orders, 
            "criterion": "canceled"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "solution": 117.72
    }
    """ test process pending """
    response = client.post(
        "/solution",
        headers={"X-Token": "coneofsilence"},
        json={
            "orders": orders, 
            "criterion": "pending"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "solution": 1004.34
    }