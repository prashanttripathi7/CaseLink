from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "change-this-before-deployment"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'linksutra.sqlite3'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REPORT_DIR = BASE_DIR / "reports"
