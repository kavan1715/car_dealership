from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.web.dependencies import get_user_service
from app.use_cases.user_service import UserService
from app.domain.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.infrastructure.security.hashing import verify_password
from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.web.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse
)

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request_data: UserRegisterRequest, 
    user_service: UserService = Depends(get_user_service)
):
    # Enforce password validations (returning 400 Bad Request as expected by tests)
    if len(request_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must be at least 8 characters long."
        )
    if request_data.password != request_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords do not match."
        )

    try:
        user = user_service.create_user(
            name=request_data.name,
            email=request_data.email,
            password=request_data.password
        )
        return user
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
def login(
    request_data: UserLoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.get_user_by_email(request_data.email)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # In our UserService, we saved the hashed password using: hashed_password = f"hashed_{password}" or bcrypt hashing.
    # Wait, the UserService implemented previously had a simple f"hashed_{password}" placeholder?
    # Ah! Previously in UserService we had: hashed_password = f"hashed_{password}" because it was Phase 4.
    # But in Phase 5 we need actual bcrypt password hashing!
    # Let's check: Yes! We should update UserService to use the proper hash_password from our hashing utility!
    # We must ensure that UserService imports and uses hash_password.
    # Let's implement the verification here first, and then we will update UserService's create_user method to use the proper hash_password!
    # Let's verify using verify_password:
    if not verify_password(request_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT Token
    token = create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role.value}
    )
    return TokenResponse(access_token=token, user=user)
