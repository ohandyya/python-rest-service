from typing import Optional, List

from fastapi import APIRouter, Query, status, BackgroundTasks, Response, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm.session import Session
from database import database
from database.db import get_db
from routers import token

router = APIRouter(
    prefix="/Activity",
    tags=["Activity"],
    responses={404: {"description": "Not found"}},
)


class ActivityAttr(BaseModel):
    male_players: int = Field(...,
                              description="Number of male players", example=5)
    female_players: int = Field(...,
                                description="Number of female players", example=2)


class Activity(ActivityAttr):
    name: str = Field(..., description="Name of the activity",
                      example="swimming")

    class Config:
        orm_mode = True


@router.get(
    "/",
    response_model=List[Activity],
    summary="Get one or all activities"
)
async def get_activity(
    response: Response,
    db: Session = Depends(get_db),
    activity: Optional[str] = Query(
        None,
        title="Activity",
        description="The name of the activity to query.",
    ),
    _: token.User = Depends(token.get_regular_user),
):
    res = database.get_activity(db, activity=activity)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
    return res


@router.put("/{name}", response_model=Activity)
async def put_activity(
    name: str,
    attr: ActivityAttr,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: token.User = Depends(token.get_regular_user),
):
    background_tasks.add_task(database.update_activity_probability, db)
    return database.put_activity(db, name, attr.dict())
