# Learning APIs Project from https://youtu.be/0sOvCWFmrtA
# Last Stop: 9:31:34
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#setting the db engine
#models.Base.metadata.create_all(bind=engine) #setup alembic so no longer required

# origins that can send API calls
origins = [
    "http://localhost",
    "http://localhost:8000"
] 

app = FastAPI()
#Passing in Cors Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#bring in our API componets routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# The root of the API
@app.get('/')
async def root():
    return {'message': 'Welcome to my API'}