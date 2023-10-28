from fastapi import FastAPI
from sqlalchemy.sql.functions import user
from router.database import engine
import router
from router import models
from fastapi.middleware.cors import CORSMiddleware
from router.router import   account,authentication

app = FastAPI()
models.Base.metadata.create_all(engine)


origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "https://vaccination-tan.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authentication.router)
app.include_router(account.router)

