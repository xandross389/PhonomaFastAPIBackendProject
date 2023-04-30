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

def test_process_orders():
    orders = [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 4.44, "status": "canceled"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 2.22, "status": "pending"}
    ]
    assert main.process_orders(orders, "completed") == 1299.69
    assert main.process_orders(orders, "pending") == 1004.34
    assert main.process_orders(orders, "canceled") == 117.72
    assert main.process_orders(orders, "all") == 2421.75
    assert main.process_orders(orders, "unknown") == 0
