import logging
import json
from typing import Optional

from fastapi import APIRouter, Path, status, Response, Depends
from sqlalchemy.orm.session import Session
from pydantic import BaseModel, Field
from database import database
from database.db import get_db
from routers import token
from model.predictor import choose_activity


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
    for row in all_activities:
        if row.gender == gender:
            # find it
            prob[row.name] = row.probability

    if not prob:
        logger.info(f"Cannot find {gender} from DB")
        return None

    # Run ML prediction
    act = choose_activity(
        list(prob.keys()),
        list(prob.values())
    )
    return act


@router.get("/{gender}", response_model=RecomActivity)
async def get_recommend_activity(
    response: Response,
    gender: str = Path(..., title="Gender", regex="^male$|^female$"),
    db: Session = Depends(get_db),
    _: token.User = Depends(token.get_regular_user),
):
    act = _recommend_activity(db, gender)

    if not act:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {
        "Activity": act,
    }
