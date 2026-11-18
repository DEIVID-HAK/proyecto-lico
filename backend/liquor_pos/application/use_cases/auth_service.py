from typing import Optional
from liquor_pos.core.domain.entities.user import User
from liquor_pos.core.ports.repositories import IUserRepository
from liquor_pos.core.ports.security import IPasswordHasher
from liquor_pos.core.domain.exceptions.base import DomainException

class InvalidCredentialsException(DomainException):
    pass

class AuthenticationService:
    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def login(self, username: str, password_plain: str) -> User:
        user = self.user_repo.get_by_username(username)
        if not user or not user.is_active:
            raise InvalidCredentialsException("Credenciales inválidas o usuario inactivo")

        if not self.password_hasher.verify(password_plain, user.password_hash):
            raise InvalidCredentialsException("Credenciales inválidas")
            
        return user
