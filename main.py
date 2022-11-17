from fastapi import FastAPI
from functions.main import _get_donatives
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


@app.get("/donatives_by_country_code")
async def get_donatives(start_date: int, country_code: str):
    """Donatives"""
    return _get_donatives(start_date, country_code)
