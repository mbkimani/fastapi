#from typing_extensions import Required

from fastapi import FastAPI

from sqlalchemy import engine

from app.oauth2 import SECRET_KEY

from . import models
from .database import engine

from .routers import posts, users, auth, vote

from .config import settings

from fastapi.middleware.cors import CORSMiddleware


#tells sqlalchemy to create all tables0
#models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()
app.add_middleware(CORSMiddleware,
allow_origins=origins,
allow_credentials = True,
allow_methods = ["*"],
allow_headers = ["*"]
)

print(settings.database_name, settings.database_username)

#point to this hash as the default hashing algo

# my_posts = [{"title":"post 1 title", "content":"post 1 content", "id": 1}, 
# {"title":"favourite dish", "content":"burger", "id": 2}]

# def printpost(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def indexposts(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message":"welcome to my api!! tots awesome.stay tuned"}




