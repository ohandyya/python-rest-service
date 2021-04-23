from typing import Optional, List

from fastapi import APIRouter, Query, status, BackgroundTasks, Response
from pydantic import BaseModel, Field
from database import database

router = APIRouter(
    prefix="/Activity",
    tags=["Activity"],
    responses={404: {"description": "Not found"}},
)


class ActivityAttr(BaseModel):
    MalePlayers: int = Field(...,
                             description="Number of male players", example=5)
    FemalePlayers: int = Field(...,
                               description="Number of female players", example=2)


class Activity(ActivityAttr):
    Name: str = Field(..., description="Name of the activity",
                      example="swimming")


@router.get("/", response_model=List[Activity])
async def get_activity(
    response: Response,
    activity: Optional[str] = Query(
        None,
        title="Activity",
        description="The name of the activity to query.",
    ),
):
    res = database.get_activity(activity=activity)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND

    return res


@router.put("/{name}", response_model=Activity)
async def put_activity(
    name: str,
    attr: ActivityAttr,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(database.update_activity_probability)
    return database.put_activity(name, attr.dict())
