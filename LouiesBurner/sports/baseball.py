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


if __name__ == "__main__":
    # for live testing & debugging only
    # must remove the . in the .sport import for this to run
    bsbl = Baseball(2024)

    # make sure that we have the season highs dataframe
    print(bsbl.season_high_df)
