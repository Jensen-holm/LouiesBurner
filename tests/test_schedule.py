import sys
import os

sys.path.append(os.path.abspath(".."))

import pytest
from louies_burner.schedule import get_schedule


def test_schedule() -> None:
    with pytest.raises(AssertionError):
        get_schedule("invalid sport")
