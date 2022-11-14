from fastapi import FastAPI
from functions.main import _get_sudan_donatives
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/sudan_donatives")
async def get_sudan_donatives():
    """Login"""
    return _get_sudan_donatives()
