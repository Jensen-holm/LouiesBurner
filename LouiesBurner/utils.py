__all__ = ["ROOT_URL", "VOLLEYBALL_ROOT_URL"]


# this is the base url for gvsu atlhetics, if we format this string
# with the name of a sport then that is the url that that sport uses.
ROOT_URL: str = "https://gvsulakers.com/sports/{sport}"

# pre formatted url for womens volleyball, not in use currently
VOLLEYBALL_ROOT_URL: str = ROOT_URL.format(sport="womens-volleyball")

# for error handling and verification, making sure we don't do stupid inputs
VALID_PAGES: set[str] = {"stats", "roster", "schedule", "coaches"}
VALID_SPORTS: set[str] = {"football", "baseball"}
