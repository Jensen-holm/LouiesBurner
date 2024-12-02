from abc import ABC, abstractmethod
import pandas as pd


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
