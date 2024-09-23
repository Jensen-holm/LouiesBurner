__all__ = ["ROOT_URL", "GVSU_ROOT_URL"]


ROOT_URL: str = "https://{school}.com/sports"

GVSU_ROOT_URL: str = ROOT_URL.format(school="gvsulakers")

VALID_SPORTS: set[str] = {"football", "baseball"}
