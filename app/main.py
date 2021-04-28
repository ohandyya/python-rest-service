import logging

from fastapi import FastAPI, Depends, Response, status

from database.db import Base, engine, DbManager
from database import database
from routers import (
    activity_probability,
    activity,
    recommender,
    token,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(activity_probability.router)
app.include_router(activity.router)
app.include_router(recommender.router)
app.include_router(token.router)


@app.get("/")
async def welcome():
    return {"message": "Main application!"}


@app.get(
    "/reset",
    description="Reset database. Require root JWT token."
)
async def reset(
    response: Response,
    _: token.User = Depends(token.get_root_user)
):
    try:
        # Initialize DB
        with DbManager() as db:
            database.initialize_activity(db)
    except Exception as e:
        logger.error(f"Reset DB failed. Error: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        msg = "Reset DB fail"
    else:
        msg = "Reset DB success"
    return {"message": msg}
