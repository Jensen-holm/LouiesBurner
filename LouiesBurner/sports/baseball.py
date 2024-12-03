import datetime
import re
from typing import Optional, List, Dict
import pandas as pd
from .sport import Sport


class Baseball(Sport):
    # these are individual box score season best indices
    _szn_high_idxs = [11, 12, 13]

    def __init__(self, year: int) -> None:
        self._year = year
        self._szn_high_df = None
        self._url = self._BASE_URL.format(
            sport="baseball",
            year=year,
        )

    @property
    def year(self) -> int:
        return self._year

    @property
    def url(self) -> str:
        return self._url

    @property
    def season_high_idxs(self) -> list[int]:
        return self._szn_high_idxs

    @property
    def season_high_df(self) -> pd.DataFrame:
        if self._szn_high_df is None:
            all_dfs = pd.read_html(self.url)
            self._szn_high_df = pd.concat(
                [df for n, df in enumerate(all_dfs) if n in self.season_high_idxs]
            )
        return self._szn_high_df

    def _extract_date(self, opponent_str: str) -> Optional[datetime.date]:
        """Extract the date from an opponent string like 'Team Name (MM/DD/YYYY)'"""
        date_match = re.search(r"\((\d{1,2}/\d{1,2}/\d{4})\)", opponent_str)
        if date_match:
            date_str = date_match.group(1)
            return datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
        return None

    def _should_tweet_stat(self, stat: str) -> bool:
        """Determine if a baseball statistic is interesting enough to tweet about."""
        # Skip negative stats
        negative_stats = [
            "STRIKEOUTS",
            "CAUGHT STEALING",
            "HIT INTO DP",
            "RUNS ALLOWED",
            "EARNED RUNS",
            "WALKS ALLOWED",
            "HITS ALLOWED",
            "DOUBLES ALLOWED",
            "TRIPLES ALLOWED",
            "HOME RUNS ALLOWED",
            "WILD PITCHES",
            "HIT BATTERS",
        ]
        return stat.upper() not in negative_stats

    def get_season_highs_for_date(self, date: datetime.date) -> List[Dict]:
        """Get baseball season highs that were set/tied on the day before the given date."""
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


if __name__ == "__main__":
    # for live testing & debugging only
    bsbl = Baseball(2024)
    print(bsbl.season_high_df)
