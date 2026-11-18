import sys
import os
import uuid

# Asegurar que el path raíz está en sys.path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from liquor_pos.infrastructure.persistence.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from liquor_pos.infrastructure.security.password_hasher import BcryptPasswordHasher
from liquor_pos.infrastructure.persistence.repositories import SQLAlchemyUserRepository
from liquor_pos.core.domain.entities.user import User, Role

def init_database():
    db_url = "sqlite:///liquor_pos.db"
    engine = get_engine(db_url)
    
    print("Creando estructura de tablas en la base de datos...")
    # Crea todas las tablas que mapeamos en models.py
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    user_repo = SQLAlchemyUserRepository(session)
    
    # Verificar si el admin ya existe para no duplicarlo
    existing_admin = user_repo.get_by_username("admin")
    if not existing_admin:
        print("Base de datos limpia. Creando usuario super-administrador (ADMIN)...")
        hasher = BcryptPasswordHasher()
        
        # Encriptando la contraseña usando bcrypt
        hashed_password = hasher.hash("admin123")
        
        admin_user = User(
            id=str(uuid.uuid4()),
            username="admin",
            password_hash=hashed_password,
            role=Role.ADMIN
        )
        
        user_repo.save(admin_user)
        session.commit()
        print("¡Usuario creado exitosamente!")
        print("  -> Username: admin")
        print("  -> Password: admin123")
    else:
        print("La base de datos ya está inicializada y el admin principal ya existe.")
        
    session.close()

if __name__ == "__main__":
    init_database()
