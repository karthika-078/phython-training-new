import os
from dotenv import load_dotenv
from matplotlib.style import context
from models import Base

load_dotenv()

config = context.config

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL not found in .env")

config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)

target_metadata = Base.metadata
