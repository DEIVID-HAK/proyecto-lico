from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

def get_engine(db_url: str):
    """
    Crea el engine de SQLAlchemy.
    Soporta PostgreSQL para producción y SQLite como fallback para desarrollo.
    """
    engine = create_engine(db_url, echo=False)
    
    if "sqlite" in db_url:
        @event.listens_for(engine, "connect")
        def do_connect(dbapi_connection, connection_record):
            # Habilitar Write-Ahead Logging para concurrencia en SQLite monousuario
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.close()
            
    return engine

def get_session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
