from LouiesBurner.sports import SPORTS, Sport
import datetime


def main(sport: str, date: datetime.date) -> None:
    sport_obj = SPORTS.get(sport, None)
    assert sport_obj is not None, f"Invalid sport '{sport}'"
    assert isinstance(sport_obj, Sport)

    sport_obj = sport_obj.__init__(year=date.year)

    # check to see if any of the season highs were set
    # in the most recent game for this sport
    ...


if __name__ == "__main__":
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-sport",
        type=str,
        options=SPORTS,
        help="name of sport to scrape",
    )

    arg_parser.add_argument(
        "-date",
        type=datetime.date.fromisoformat,
        help="Date in ISO format (YYYY-MM-DD). The previous date will be checked",
        default=datetime.date.today().isoformat(),
    )

    # parse arguments, and unpack them into main function
    _ = main(**arg_parser.parse_args().__dict__)
