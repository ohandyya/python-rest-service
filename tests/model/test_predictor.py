import pytest

from model.predictor import choose_activity


@pytest.mark.parametrize(
    "activities, probs, seed, exp_activity",
    [
        (["a", "b"], [1.0, 0.0], None, "a"),
        (["a", "b"], [0.5, 0.5], 0, "b"),
    ]
)
def test_choose_activity(activities, probs, seed, exp_activity):
    activity = choose_activity(activities, probs, seed=seed)
    assert activity == exp_activity
