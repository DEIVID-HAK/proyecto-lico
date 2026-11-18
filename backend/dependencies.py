from sqlalchemy.orm import Session
from liquor_pos.infrastructure.persistence.database import get_engine, get_session_factory, Base
from liquor_pos.infrastructure.persistence.models import *

# Setup Database (Using SQLite for now, as configured)
engine = get_engine("sqlite:///liquor_pos.db")
Base.metadata.create_all(bind=engine)
SessionFactory = get_session_factory(engine)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
