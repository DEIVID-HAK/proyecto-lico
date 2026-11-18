import bcrypt
from liquor_pos.core.ports.security import IPasswordHasher

class BcryptPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        # Genera el hash de forma segura con un salt aleatorio
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
