import os


class Config:
    _base_dir = os.environ.get(
        "SQLLITE_PATH", f"sqlite://{os.path.expanduser('~')}/.awesome"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", f"{_base_dir}/awesome.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
