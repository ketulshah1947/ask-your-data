import os
from src.logger import logger
from sqlalchemy import create_engine

db_url = os.getenv("DB_URL") or "postgresql://ketul:secret@localhost:5432/ecommerce"
logger.info(f"db_url: {db_url}")
db_engine = create_engine(db_url)
