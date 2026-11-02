from pathlib import Path


APP_NAME = "Leafwise"
APP_TAGLINE = "Plant health and crop guidance"
ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_DIR / "trained_plant_disease_model.keras"
HISTORY_PATH = ROOT_DIR / "training_hist.json"
DATASET_DIR = ROOT_DIR / "dataset"
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"
SAMPLE_DIR = STATIC_DIR / "samples"

MAX_UPLOAD_BYTES = 8 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
WIKI_USER_AGENT = "Leafwise/1.0 (local plant-health educational project)"
WIKI_TIMEOUT = (4, 14)
WIKI_CACHE_TTL = 6 * 60 * 60

CONFIDENCE_HIGH = 0.80
CONFIDENCE_MODERATE = 0.55

SOURCES = {
    "wikipedia": {
        "name": "Wikipedia",
        "url": "https://en.wikipedia.org/",
        "api_url": "https://www.mediawiki.org/wiki/API:Main_page",
        "note": "Cultivation and disease-management passages are read from the public Wikipedia API at request time. Text is available under CC BY-SA.",
    },
}
