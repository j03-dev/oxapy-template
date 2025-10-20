from oxapy import jwt  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()

ADDR = ("0.0.0.0", 8000)

STATIC_DIR = "static"

DATABASE_URL = os.getenv("DATABASE_URL")
TURSO_DB_URL = os.getenv("TURSO_DB_URL")
TURSO_DB_AUTH_TOKEN = os.getenv("TURSO_DB_AUTH_TOKEN")

ENGINE = create_engine(
    DATABASE_URL,  # type: ignore
    connect_args={
        "sync_url": TURSO_DB_URL,
        "auth_token": TURSO_DB_AUTH_TOKEN,
    },
)

DB = sessionmaker(bind=ENGINE)

SECRET_KEY = os.getenv("SECRET_KEY")

JWT = jwt.Jwt(SECRET_KEY)  # type: ignore
