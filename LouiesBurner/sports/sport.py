from abc import ABC, abstractmethod
import datetime
import pandas as pd
from typing import List, Dict


class Sport(ABC):
    _BASE_URL = "https://gvsulakers.com/sports/{sport}/stats/{year}"
    __slots__ = ["_year", "_url", "_szn_high_idxs", "_szn_high_df"]

    @property
    @abstractmethod
    def year(self) -> int:
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @property
    @abstractmethod
    def season_high_idxs(self) -> list[int]:
        pass

    @property
    @abstractmethod
    def season_high_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_season_highs_for_date(self, date: datetime.date) -> List[Dict]:
        """
        Get season highs that were set/tied on the day before the given date.

        Args:
            date: The date to check for season highs (will check previous day)

        Returns:
            List of dictionaries containing season high information:
            [
                {
                    'Statistic': str,  # Name of the statistic
                    'Value': float,    # Value achieved
                    'Player': str,     # Player who achieved it
                    'Opponent': str,   # Opponent it was achieved against
                    'Date': datetime.date  # Date it was achieved
                },
                ...
            ]
        """
        pass
