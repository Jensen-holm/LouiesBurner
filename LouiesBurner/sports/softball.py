import datetime
import re
import random
from typing import Optional, List, Dict
import pandas as pd
from .sport import Sport


# Skip negative stats for softball
negative_stats = [
    "STRIKEOUTS",
    "CAUGHT STEALING",
    "HIT INTO DP",
]


class Softball(Sport):
    """
    Class for handling softball-specific statistics and tweet generation.

    This class extends the base Sport class with softball-specific implementations
    for processing season highs and creating engaging tweets.

    Attributes
    ----------
    _szn_high_idxs : list[int]
        Indices of season high tables in the scraped data
    """

    _szn_high_idxs = [11]

    def __init__(self, year: int) -> None:
        """
        Initialize a Softball instance.

        Parameters
        ----------
        year : int
            The year for which to fetch softball statistics
        """
        super().__init__(year=year, sport="softball")

    def _extract_date(self, opponent_str: str) -> Optional[datetime.date]:
        """
        Extract the date from an opponent string.

        Parameters
        ----------
        opponent_str : str
            String containing opponent name and date in format 'Team Name (MM/DD/YYYY)'

        Returns
        -------
        Optional[datetime.date]
            The extracted date if found, None otherwise
        """
        date_match = re.search(r"\((\d{1,2}/\d{1,2}/\d{4})\)", opponent_str)
        if date_match:
            date_str = date_match.group(1)
            return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
        return None

    def _should_tweet_stat(self, stat: str) -> bool:
        """
        Determine if a softball statistic is interesting enough to tweet about.

        Parameters
        ----------
        stat : str
            The name of the statistic to evaluate

        Returns
        -------
        bool
            True if the stat should be tweeted, False if it's in negative_stats
        """
        return stat.upper() not in negative_stats

    def _get_softball_verb(self, stat: str) -> str:
        """
        Get an appropriate verb for a softball statistic.

        Parameters
        ----------
        stat : str
            The name of the statistic

        Returns
        -------
        str
            An appropriate verb for the given statistic

        Notes
        -----
        Returns specific verbs for different types of stats:
        - "finished with" for at bats
        - "racked up" for hits, runs scored, RBIs
        - "crushed" for home runs, doubles, triples
        - etc.
        """
        stat = stat.lower()
        if stat in ["at bats"]:
            return "finished with"
        elif stat in ["hits", "runs scored", "rbis"]:
            return "racked up"
        elif stat in ["home runs", "doubles", "triples"]:
            return "crushed"
        elif stat in ["stolen bases"]:
            return "swiped"
        elif stat in ["walks"]:
            return "drew"
        elif stat in ["sac hits", "sac flies"]:
            return "executed"
        elif stat in ["hit by pitch"]:
            return "took one for the team with"
        return "recorded"

    def create_tweet_text(self, highs: list[dict]) -> str:
        """
        Create an engaging tweet about softball season high achievement(s).

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
        Uses softball-specific templates and hashtags (#GLVCsb).
        Handles both single and multiple achievements by the same player.
        """
        player = highs[0]["Player"]
        assert isinstance(player, str)

        if all(h["Player"] == player for h in highs):
            if len(highs) == 1:
                high = highs[0]
                single_templates = [
                    "🥎 SEASON HIGH ALERT! 🥎\n{player} just {verb} {value} {stat_type} against {opponent}! #AnchorUp ⚓️",
                    "🔥 {player} is ON FIRE! 🔥\nJust set a season high with {value} {stat_type} vs {opponent}! #AnshorUp ⚓️",
                    "⚡️ RECORD BREAKER ⚡️\n{player} leads the way with {value} {stat_type} against {opponent}! #AnchorUp ⚓️",
                    "👀 Look what {player} just did!\nNew season high: {value} {stat_type} vs {opponent}! #AnchorUp ⚓️",
                    "💪 BEAST MODE: {player} 💪\nDominates with {value} {stat_type} against {opponent}! #AnchorUp ⚓️",
                ]

                return random.choice(single_templates).format(
                    player=high["Player"],
                    value=high["Value"],
                    stat_type=high["Statistic"].lower(),
                    opponent=re.sub(r"\s*\([^)]*\)", "", high["Opponent"]),
                    verb=self._get_softball_verb(high["Statistic"]),
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
                    "🥎 WHAT A GAME! 🥎\n{player} sets multiple season highs with {achievements} against {opponent}! #AnchorUp #GLVCsb ⚓️",
                    "⚡️ {player} IS UNSTOPPABLE! ⚡️\nNew season highs: {achievements} vs {opponent}! #GLVCsb",
                    "💪 DOMINANT PERFORMANCE 💪\n{player} sets new highs with {achievements} against {opponent}! #AnchorUp #GLVCsb",
                ]
                return random.choice(multi_templates).format(
                    player=player,
                    achievements=achievements_str,
                    opponent=re.sub(r"\s*\([^)]*\)", "", highs[0]["Opponent"]),
                )

        # If we somehow get here (shouldn't with current logic), use a simple template
        high = highs[0]
        return f"🥎 New season high! {high['Player']} {self._get_softball_verb(high['Statistic'])} {high['Value']} {high['Statistic'].lower()} against {re.sub(r'\s*\([^)]*\)', '', high['Opponent'])}! #AnchorUp #GLVCsb"

    def get_season_highs_for_date(self, date: datetime.date) -> List[Dict]:
        """
        Get softball season highs that were set/tied on the day before the given date.

        Parameters
        ----------
        date : datetime.date
            The date to check for season highs (will check previous day)

        Returns
        -------
        List[Dict]
            List of dictionaries containing season high information:
            - Statistic : str
                Name of the statistic
            - Value : Any
                Value achieved
            - Player : str
                Player who achieved it
            - Opponent : str
                Opponent it was achieved against
            - Date : datetime.date
                Date it was achieved

        Notes
        -----
        Filters out negative statistics (defined in negative_stats list)
        and only includes achievements from the previous day.
        """
        # Get the previous day's date
        prev_date = date - datetime.timedelta(days=1)

        # Get the season highs dataframe
        df = self.season_high_df

        # Track any new or tied season highs
        new_highs = []

        # Process each row in the dataframe
        for _, row in df.iterrows():
            statistic = row["Statistic"]

            # Skip stats we don't want to tweet about
            if not self._should_tweet_stat(statistic):
                continue

            high_value = row["High"]
            players = row["Player"].split("; ")
            opponents = row["Opponent"].split("; ")

            # Check each player/opponent combination for this statistic
            for player, opponent in zip(players, opponents):
                game_date = self._extract_date(opponent)

                # Only include achievements from the previous day
                if game_date and game_date == prev_date:
                    new_highs.append(
                        {
                            "Statistic": statistic,
                            "Value": high_value,
                            "Player": player,
                            "Opponent": opponent,
                            "Date": game_date,
                        }
                    )

        return new_highs
