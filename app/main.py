from fastapi import FastAPI

from routers import (
    activity_probability,
    activity,
)

app = FastAPI()

app.include_router(activity_probability.router)
app.include_router(activity.router)


@app.get("/")
async def root():
    return {"message": "Main application!"}
