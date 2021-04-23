# Contains the interface for DB access
import logging
from typing import Dict, List, Optional, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Dummy database for developing purpose
Table_Activity = [
    {
        "Name": "swimming",
        "MalePlayers": 1,
        "FemalePlayers": 2,
    },
    {
        "Name": "basketball",
        "MalePlayers": 25,
        "FemalePlayers": 10,
    },
]

Table_Activity_Probability = [
    {
        "Gender": "male",
        "ActivityProbability": {
            "basketball": 0.8,
            "swimming": 0.2,
            "dummy": 0.0,
        },
    },
    {
        "Gender": "female",
        "ActivityProbability": {
            "swimming": 0.7,
            "shopping": 0.3,
        },
    },
]


def get_activity_probability() -> Dict[str, Dict[str, float]]:
    """ Return all items from the ActivityProbability table"""
    res = {}
    for row in Table_Activity_Probability:
        if row["Gender"] == "male":
            res["male"] = row["ActivityProbability"]
        elif row["Gender"] == "female":
            res["female"] = row["ActivityProbability"]
        else:
            pass

    return res


def get_activity(activity: Optional[str] = None) -> List[Dict[str, Union[str, int]]]:
    """Return activity"""
    if activity:
        res = [act.copy() for act in Table_Activity if act["Name"] == activity]
        return res
    else:
        return Table_Activity.copy()


def put_activity(name: str, attr: dict) -> Dict[str, Union[str, int]]:
    """Update activity"""
    new_act = {
        "Name": name,
        "MalePlayers": attr["MalePlayers"],
        "FemalePlayers": attr["FemalePlayers"],
    }
    is_updated = False
    for act in Table_Activity:
        if name == act["Name"]:
            act["MalePlayers"] = new_act["MalePlayers"]
            act["FemalePlayers"] = new_act["FemalePlayers"]
            is_updated = True
            break

    if not is_updated:
        Table_Activity.append(new_act)

    logger.info(Table_Activity)

    return new_act


def compute_activity_probability(
    activities: List[Dict[str, Union[str, int]]]
) -> List[dict]:
    """Compute activity probability table based on activities"""
    all_genders = ["male", "female"]
    prob = {
        "male": {},
        "female": {},
    }

    for activity in activities:
        for gender, cnt_key in zip(all_genders, ["MalePlayers", "FemalePlayers"]):
            prob[gender][activity["Name"]] = activity[cnt_key]

    # Compute probability
    for gender in all_genders:
        total_cnt = sum(prob[gender].values())
        for name in prob[gender]:
            prob[gender][name] /= total_cnt

    return prob


def update_activity_probability():
    logger.info("Updating activity probability table")
    # Get the current activity table
    activities = get_activity()

    # Compute the new activity probability
    activity_probability = compute_activity_probability(activities)

    # Update table
    for row in Table_Activity_Probability:
        row["ActivityProbability"] = activity_probability[row["Gender"]]

    logger.info(Table_Activity_Probability)
