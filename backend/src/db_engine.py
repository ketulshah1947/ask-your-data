import os

from sqlalchemy import create_engine

db_engine = create_engine(os.getenv("DB_URL") or "postgresql://ketul:secret@localhost:5432/ecommerce")
