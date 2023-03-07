from api.routers import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database

origins = [
    'http://localhost',
    'http://localhost:8000',
]

app = FastAPI(title="Complaint System")
app.include_router(api_router)
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.on_event("startup")
async def startup():
    print("Startup")
    await database.connect()
    print("Connected to database")


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")
    await database.disconnect()
    print("Disconnected from database")
