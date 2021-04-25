from typing import Dict
import json

from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel, Field
from database import database
from sqlalchemy.orm.session import Session
from database.db import get_db


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
async def get_activity_probability(response: Response, db: Session = Depends(get_db)):
    raw_res = database.get_activity_probability(db)
    if not raw_res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    # Convert raw_res to ActivityProbability
    res = {}
    for row in raw_res:
        res[row.gender] = json.loads(row.probability)
    return res
