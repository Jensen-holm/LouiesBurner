from abc import ABC, abstractmethod
import datetime
import random
import re
import pandas as pd
from typing import Any


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

    def create_tweet_text(self, highs: list[dict]) -> str:
        """
        Create an engaging tweet about season high achievement(s).
        This is a default implementation that can be overridden by specific sports.
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
