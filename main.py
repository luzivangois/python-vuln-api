from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# @app.post("/register")
# def register(name: str, login: str, password: str, role: str):
