import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from routes import views

app = FastAPI()

app.include_router(views.router)
