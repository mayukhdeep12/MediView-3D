import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mediview-3d_server import mediview-3dApi

# Import the mediview-3d example API
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from example_api import mediview-3d


app = FastAPI()

# Adds mediview-3d middlware
app.add_middleware(mediview-3d)

# Set CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get("/")
def index():
    return {"hello": "world"}
