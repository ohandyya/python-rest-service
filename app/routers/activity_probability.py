from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel, Field
from database import database

router = APIRouter(
    prefix="/ActivityProbability",
    tags=["ActivityProbability"],
    responses={404: {"description": "Not found"}},
)


class ActivityProbability(BaseModel):
    male: Dict[str, float] = Field(
        ...,
        example={
            "basketball": 0.8,
            "swimming": 0.2,
        },
    )
    female: Dict[str, float] = Field(
        ...,
        example={
            "walking": 0.5,
            "shopping": 0.5,
        }
    )


@router.get("/", response_model=ActivityProbability)
async def get_activity_probability():
    return database.get_activity_probability()
