from fastapi import FastAPI
from app.controllers.analysis_controller import analysis_router

app = FastAPI()
app.include_router(analysis_router)
