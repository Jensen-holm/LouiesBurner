from .sport import Sport


class Soccer(Sport):
    _szn_high_idxs = [17]

    def __init__(self, year: int) -> None:
        super().__init__(year=year, sport="womens-soccer")
