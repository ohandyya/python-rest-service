import logging
from typing import List, Optional
import numpy as np


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    # Ensure probs sum to 1
    total_sum = sum(probs)
    if total_sum > 0:
        modified_probs = [val / total_sum for val in probs]
    else:
        # something is wrong as the sum of all probs should be close to 1
        logger.warning(
            "Received selection probability that sums less than 0. "
            f"Expected the sum to be close to 1. "
            f"selection probability = {probs}. Choose an activity uniformlly."
        )
        modified_probs = None

    act = rng.choice(
        activities,
        p=modified_probs
    )
    return act
