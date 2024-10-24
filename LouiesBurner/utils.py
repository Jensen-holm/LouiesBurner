__all__ = ["ROOT_URL", "VOLLEYBALL_ROOT_URL"]


ROOT_URL: str = "https://gvsulakers.com/sports/{sport}"

SOCCER_ROOT_URL: str = ROOT_URL.format(sport="womens-soccer")

VALID_PAGES: set[str] = {"stats", "roster", "schedule", "coaches"}
VALID_SPORTS: set[str] = {"football", "baseball"}
