# Contains the interface for DB access
import logging
import json
from sqlalchemy.orm import Session
from typing import List, Optional

from database import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_activity(db: Session):
    # Delete all current records
    db.query(models.Activity).delete()
    db.commit()

    # Add new records in activity table
    db_activity = models.Activity(
        name="swimming", male_players=3, female_players=5)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    db_activity = models.Activity(
        name="basketball", male_players=10, female_players=3)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    # Update activity probability table
    update_activity_probability(db)


def get_activity_probability(db: Session) -> List[models.ActivityProbability]:
    """ Return all items from the ActivityProbability table"""
    try:
        res_all = db.query(models.ActivityProbability).all()
    except Exception as e:
        logger.error(f"DB query failed. Error: {e}")
        return []

    return res_all


def get_activity(db: Session, activity: Optional[str] = None) -> List[models.Activity]:
    """Return activity"""
    if activity:
        try:
            res_all = db.query(models.Activity).filter(
                models.Activity.name == activity).all()
        except Exception as e:
            logger.error(f"DB query failed. Error: {e}")
            return []
        return res_all
    else:
        try:
            res_all = db.query(models.Activity).all()
        except Exception as e:
            logger.error(f"DB query failed. Error: {e}")
            return []
        return res_all


def put_activity(db: Session, name: str, attr: dict) -> models.Activity:
    """Update activity"""
    new_act = models.Activity(
        name=name,
        **attr,
    )
    cur_act = db.query(models.Activity).filter(
        models.Activity.name == name).first()
    if cur_act:
        # found existing activity
        for key, val in attr.items():
            setattr(cur_act, key, val)
        db.commit()
    else:
        # new activity
        db.add(new_act)
        db.commit()
        db.refresh(new_act)
    return new_act


def compute_activity_probability(
    activities: List[models.Activity]
) -> dict:
    """Compute activity probability table based on activities

    Return Example:

    {
        "male": {
                "basketball": 0.8,
                "swimming": 0.2,
                "dummy": 0.0,
        },
        "female": {
                "swimming": 0.7,
                "shopping": 0.3,
        },
    }
    """
    all_genders = ["male", "female"]
    prob = {
        "male": {},
        "female": {},
    }

    for activity in activities:
        for gender, cnt_key in zip(all_genders, ["male_players", "female_players"]):
            prob[gender][getattr(activity, "name")] = getattr(
                activity, cnt_key)

    # Compute probability
    for gender in all_genders:
        total_cnt = sum(prob[gender].values())
        for name in prob[gender]:
            prob[gender][name] /= total_cnt

    return prob


def update_activity_probability(db: Session):
    # Delete all current records
    db.query(models.ActivityProbability).delete()
    db.commit()

    logger.info("Updating activity probability table")
    # Get the current activity table
    activities = get_activity(db)

    # Compute the new activity probability
    activity_probability = compute_activity_probability(activities)

    # Update table
    for gender, gender_probs in activity_probability.items():
        try:
            db_record = models.ActivityProbability(
                gender=gender,
                probability=json.dumps(gender_probs)
            )
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
        except Exception as e:
            logger.error(f"Update db failed. Error: {e}")
