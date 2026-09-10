from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
APP_CONFIG = {
    "name": os.getenv("APP_NAME", "DataPilot Global"),
    "brand_name": os.getenv("BRAND_NAME", "DataPilot Analytics"),
    "max_upload_mb": int(os.getenv("MAX_UPLOAD_MB", "200")),
    "default_missing_numeric": os.getenv("DEFAULT_MISSING_NUMERIC", "median"),
}
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xlsm", "xls"}
MAX_ROWS_FOR_HEAVY_CHARTS = 250_000
