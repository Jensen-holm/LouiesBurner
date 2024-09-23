from .utils import VALID_SPORTS


def get_schedule(sport: str):
    assert sport in VALID_SPORTS, f"invalid sport '{sport}'"
