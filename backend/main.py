from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from liquor_pos.infrastructure.persistence.repositories import SQLAlchemyUserRepository
from liquor_pos.infrastructure.security.password_hasher import BcryptPasswordHasher
from liquor_pos.application.use_cases.auth_service import AuthenticationService, InvalidCredentialsException

from dependencies import get_db
from routers import products

app = FastAPI(title="Liquor POS API", version="1.0.0")

app.include_router(products.router)

# Dependency Injection for Authentication Service
def get_auth_service(db: Session = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(db)
    password_hasher = BcryptPasswordHasher()
    return AuthenticationService(user_repo, password_hasher)

# Pydantic models for API requests/responses
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    role: str
    
    class Config:
        from_attributes = True

@app.post("/api/auth/login", response_model=UserResponse)
def login(request: LoginRequest, auth_service: AuthenticationService = Depends(get_auth_service)):
    try:
        user = auth_service.login(request.username, request.password)
        # Handle Enum value extraction if user.role is an Enum
        role_value = user.role.value if hasattr(user.role, 'value') else str(user.role)
        return UserResponse(username=user.username, role=role_value)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
