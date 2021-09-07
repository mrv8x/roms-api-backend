from typing import Dict
from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

TELEGRAPH_DOMAIN = "https://telegra.ph/"


def get_changelog(obj: Dict):
    if not obj["changelog"].startswith(TELEGRAPH_DOMAIN):
        return obj["changelog"]

    telegraph = Telegraph()
    html_data: str = None

    try:
        request = telegraph.get_page(obj["changelog"].replace(TELEGRAPH_DOMAIN, ""))
        html_data = request["content"]
    except TelegraphException:
        return "Cannot get changelog"

    return html_data
