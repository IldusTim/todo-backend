import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

from resources import Entry, EntryManager

app = FastAPI()

origins = [
    "https://wexler.io"  # адрес на котором работает фронт-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список разрешенных доменов
    allow_credentials=True,  # Разрешить Cookies и Headers
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все хедеры
)

# выставление переменной среды, можно выставить через IDE
os.environ['data_folder'] = '/kuku/'


class Settings(BaseSettings):
    data_folder: str = '/files/'


settings = Settings()


@app.get("/")
async def hello_world():
    return {"Hello": "World"}


@app.get("/api/entries/")
async def get_entries():
    em = EntryManager(settings.data_folder)
    em.load()
    return [e.json() for e in em.entries]


@app.post("/api/save_entries/")
async def save_entries(data: list[dict]):
    em = EntryManager(settings.data_folder)
    em.entries = [Entry.from_json(val) for val in data]
    em.save()
    return {'status': 'success'}


@app.get('/api/get_data_folder/')
async def get_data_folder():
    return {'folder': settings.data_folder}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
