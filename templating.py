from datetime import datetime
from urllib.parse import urlencode

from fastapi.templating import Jinja2Templates

from webapp.config import APP_NAME, APP_TAGLINE, SOURCES, TEMPLATE_DIR
from webapp.data.samples import SAMPLES


templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

NAV_ITEMS = (
    {"key": "home", "label": "Home", "href": "/"},
    {"key": "diagnose", "label": "Diagnose", "href": "/diagnose"},
    {"key": "guide", "label": "Crop guide", "href": "/guide"},
    {"key": "about", "label": "About", "href": "/about"},
)


def percent(value, digits: int = 1) -> str:
    if value is None:
        return "—"
    return f"{float(value) * 100:.{digits}f}%"


def query_url(path: str, **params) -> str:
    clean = {
        key: value
        for key, value in params.items()
        if value is not None and value != ""
    }
    return f"{path}?{urlencode(clean)}" if clean else path


templates.env.filters["percent"] = percent
templates.env.globals["query_url"] = query_url
templates.env.globals.update(
    app_name=APP_NAME,
    app_tagline=APP_TAGLINE,
    nav_items=NAV_ITEMS,
    sources=SOURCES,
    samples=SAMPLES,
    current_year=datetime.now().year,
)
