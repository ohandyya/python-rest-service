import logging
import json
from typing import Optional

import numpy as np
from fastapi import APIRouter, Path, status, Response, Depends
from sqlalchemy.orm.session import Session
from pydantic import BaseModel, Field
from database import database
from database.db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/Recommender",
    tags=["Recommender"],
    responses={404: {"description": "Not found"}},
)


class RecomActivity(BaseModel):
    Activity: Optional[str] = Field(
        None,
        description="Recommended activity",
        example="swimming"
    )


def _recommend_activity(db: Session, gender: str) -> Optional[str]:
    """Recommend activity based on gender"""
    all_activities = database.get_activity_probability(db)

    # Get all activities for gender
    prob = {}
    for gender_prob in all_activities:
        if gender_prob.gender == gender:
            # find it
            prob = json.loads(gender_prob.probability)
            break

    if not prob:
        logger.info(f"Cannot find {gender} from DB")
        return None

    # This block simulate a simple ML algorithm
    # In real life, we will put the ML algrotihm in a different file/package
    rng = np.random.default_rng()
    act = rng.choice(
        list(prob.keys()),
        p=list(prob.values())
    )
    return act


@router.get("/{gender}", response_model=RecomActivity)
async def get_recommend_activity(
    response: Response,
    gender: str = Path(..., title="Gender", regex="^male$|^female$"),
    db: Session = Depends(get_db),
):
    act = _recommend_activity(db, gender)

    if not act:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {
        "Activity": act,
    }
