import logging

from fastapi import FastAPI

from database.db import Base, engine, DbManager
from database import database
from routers import (
    activity_probability,
    activity,
    recommender
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(activity_probability.router)
app.include_router(activity.router)
app.include_router(recommender.router)


@app.get("/")
async def root():
    return {"message": "Main application!"}


@app.get("/reset")
async def reset():
    try:
        # Initialize DB
        with DbManager() as db:
            database.initialize_activity(db)
    except Exception as e:
        logger.error(f"Reset DB failed. Error: {e}")
        msg = "Reset DB failed"
    else:
        msg = "Reset DB success"
    return {"message": msg}
