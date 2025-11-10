from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.models.user import (
    User, UserCreate, UserRead, UserLogin, UserProfile,
    TokenResponse, RefreshTokenRequest, ChangePasswordRequest, UserUpdate
)
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token, decode_token, verify_token_type
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    request: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user
    
    Automatically creates default chart of accounts for the new user
    """
    user = UserService.create_user(
        session=session,
        email=request.email,
        name=request.name,
        password=request.password
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    request: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Login with email and password, returns JWT tokens
    """
    user = UserService.authenticate_user(
        session=session,
        email=request.email,
        password=request.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    session: Session = Depends(get_session)
):
    """
    Refresh access token using refresh token
    """
    # Decode refresh token
    payload = decode_token(request.refresh_token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify token type
    if not verify_token_type(payload, "refresh"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    # Get user_id
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Verify user exists
    user = UserService.get_user_by_id(session, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Create new tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token
    )


@router.get("/me", response_model=UserProfile)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user profile
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID is missing"
        )
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name
    )


@router.patch("/me", response_model=UserProfile)
def update_me(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update current user profile
    
    **Requires authentication**
    """
    updated_user = UserService.update_user(
        session=session,
        user=current_user,
        name=request.name,
        email=request.email
    )
    
    if updated_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID is missing"
        )
    
    return UserProfile(
        id=updated_user.id,
        email=updated_user.email,
        name=updated_user.name
    )


@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Change current user's password
    
    **Requires authentication**
    """
    UserService.change_password(
        session=session,
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password
    )
    
    return {"message": "Password changed successfully"}


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout (client should discard tokens)
    
    **Requires authentication**
    
    Note: JWT tokens are stateless, so logout is handled client-side
    """
    return {"message": "Logged out successfully"}