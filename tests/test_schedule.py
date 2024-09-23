import sys
import os

sys.path.append(os.path.abspath(".."))

import pytest
from LouiesBurner.schedule import get_schedule


def test_schedule() -> None:
    with pytest.raises(AssertionError):
        get_schedule("invalid sport")
