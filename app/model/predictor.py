from typing import List, Optional
import numpy as np


def choose_activity(
    activities: List[str],
    probs: List[float],
    seed: Optional[int] = None,
) -> str:
    """Choose an activity based on probability

    Args:
        activities (List[str]): [description]
        probs (List[float]): [description]

    Returns:
        str: [description]
    """
    rng = np.random.default_rng(seed=seed)
    act = rng.choice(
        activities,
        p=probs
    )
    return act
