from abc import ABC, abstractmethod
import datetime
import random
import re
import pandas as pd
from typing import Any


class Sport(ABC):
    """
    Abstract base class for sports data processing.

    This class provides the foundation for sport-specific implementations,
    handling season high statistics and tweet generation.

    Attributes
    ----------
    _BASE_URL : str
        Base URL template for fetching sports statistics
    """

    _BASE_URL = "https://gvsulakers.com/sports/{sport}/stats/{year}"
    __slots__ = ["_year", "_url", "_szn_high_idxs", "_szn_high_df"]

    def __init__(self, year: int, sport: str) -> None:
        """
        Initialize a Sport instance.

        Parameters
        ----------
        year : int
            The year for which to fetch statistics
        sport : str
            The sport identifier used in the URL
        """
        self._year = year
        self._szn_high_df = None
        self._url = self._BASE_URL.format(
            year=year,
            sport=sport,
        )

    @property
    def year(self) -> int:
        """
        Get the year for which statistics are being tracked.

        Returns
        -------
        int
            The year of the statistics
        """
        return self._year

    @property
    def url(self) -> str:
        """
        Get the URL for fetching sports statistics.

        Returns
        -------
        str
            The complete URL for fetching statistics
        """
        return self._url

    @property
    def season_high_idxs(self) -> list[int]:
        """
        Get the indices of season high tables in the scraped data.

        Returns
        -------
        list[int]
            List of indices corresponding to season high tables
        """
        return self._szn_high_idxs

    @property
    def season_high_df(self) -> pd.DataFrame:
        """
        Get the DataFrame containing season high statistics.

        Lazily loads the data from the URL if not already loaded.

        Returns
        -------
        pd.DataFrame
            DataFrame containing season high statistics
        """
        if self._szn_high_df is None:
            all_dfs = pd.read_html(self.url)
            self._szn_high_df = pd.concat(
                [df for n, df in enumerate(all_dfs) if n in self._szn_high_idxs]
            )
        return self._szn_high_df

    def create_tweet_text(self, highs: list[dict]) -> str:
        """
        Create an engaging tweet about season high achievement(s).

        Parameters
        ----------
        highs : list[dict]
            List of dictionaries containing achievement information.
            Each dictionary should contain:
            - Player: str, name of the player
            - Value: Any, the value achieved
            - Statistic: str, type of statistic
            - Opponent: str, opposing team

        Returns
        -------
        str
            Formatted tweet text describing the achievement(s)

        Notes
        -----
        This is a default implementation that can be overridden by specific sports.
        Handles both single and multiple achievements by the same player.
        """
        # If multiple achievements by same player, combine them
        player = highs[0]["Player"]
        assert isinstance(player, str)

        if all(h["Player"] == player for h in highs):
            if len(highs) == 1:
                high = highs[0]
                single_templates = [
                    "🚨 SEASON HIGH ALERT! 🚨\n{player} just recorded {value} {stat_type} against {opponent}! #AnchorUp ⚓️",
                    "🔥 {player} is ON FIRE! 🔥\nJust set a season high with {value} {stat_type} vs {opponent}! #AnchorUp",
                    "⚡️ RECORD BREAKER ⚡️\n{player} leads the way with {value} {stat_type} against {opponent}! #AnchorUp",
                    "👀 Look what {player} just did!\nNew season high: {value} {stat_type} vs {opponent}! #AnchorUp ⚓️",
                    "💪 BEAST MODE: {player} 💪\nDominates with {value} {stat_type} against {opponent}! #AnchorUp",
                ]

                return random.choice(single_templates).format(
                    player=high["Player"],
                    value=high["Value"],
                    stat_type=high["Statistic"].lower(),
                    opponent=re.sub(r"\s*\([^)]*\)", "", high["Opponent"]),
                )
            else:
                # Combine multiple achievements
                achievements = []
                for high in highs:
                    stat = high["Statistic"].lower()
                    achievements.append(f"{high['Value']} {stat}")
                achievements_str = (
                    ", ".join(achievements[:-1]) + f" and {achievements[-1]}"
                )
                multi_templates = [
                    "🔥 WHAT A GAME! 🔥\n{player} sets multiple season highs with {achievements} against {opponent}! #AnchorUp ⚓️",
                    "⚡️ {player} IS UNSTOPPABLE! ⚡️\nNew season highs: {achievements} vs {opponent}! #AnchorUp",
                    "💪 DOMINANT PERFORMANCE 💪\n{player} sets new highs with {achievements} against {opponent}! #AnchorUp",
                ]
                return random.choice(multi_templates).format(
                    player=player,
                    achievements=achievements_str,
                    opponent=re.sub(r"\s*\([^)]*\)", "", highs[0]["Opponent"]),
                )

        # If we somehow get here (shouldn't with current logic), use a simple template
        high = highs[0]
        return f"🎯 New season high! {high['Player']} recorded {high['Value']} {high['Statistic'].lower()} against {re.sub(r'\s*\([^)]*\)', '', high['Opponent'])}! #AnchorUp"

    @abstractmethod
    def get_season_highs_for_date(self, date: datetime.date) -> list[dict[str, Any]]:
        """
        Get season highs that were set/tied on the day before the given date.

        Parameters
        ----------
        date : datetime.date
            The date to check for season highs (will check previous day)

        Returns
        -------
        list[dict[str, Any]]
            List of dictionaries containing season high information:
            - Statistic : str
                Name of the statistic
            - Value : float
                Value achieved
            - Player : str
                Player who achieved it
            - Opponent : str
                Opponent it was achieved against
            - Date : datetime.date
                Date it was achieved
        """
        pass
