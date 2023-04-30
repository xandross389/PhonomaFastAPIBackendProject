#####
# Filename: main.py
# Created Date: Saturday, April 29th 2023, 8:44:33 pm
# Author: Alejandro Gómez Jiménez (xandross389@gmail.com)
# -----
# Copyright (c) 2023 - MIT License
# -----
# Last Modified: Sat Apr 29 2023
# Modified By: Alejandro Gómez Jiménez
#####

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}