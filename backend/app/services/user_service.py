from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password, verify_password
from typing import Optional


class UserService:
    """Service layer for user operations"""
    
    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user
    
    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user
    
    @staticmethod
    def create_user(session: Session, email: str, name: str, password: str) -> User:
        """Create a new user and seed default accounts"""
        # Check if user already exists
        existing_user = UserService.get_user_by_email(session, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            name=name,
            password_hash=hashed_password
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Create default accounts for new user
        from app.utils.seed_accounts import create_default_accounts
        if user.id is not None:
            create_default_accounts(session, user.id)
        
        return user
    
    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = UserService.get_user_by_email(session, email)
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def update_user(
        session: Session, 
        user: User, 
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> User:
        """Update user profile"""
        if name:
            user.name = name
        
        if email and email != user.email:
            # Check if new email already exists
            existing_user = UserService.get_user_by_email(session, email)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            user.email = email
        
        from datetime import datetime
        user.updated_at = datetime.utcnow()
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user
    
    @staticmethod
    def change_password(
        session: Session,
        user: User,
        current_password: str,
        new_password: str
    ) -> User:
        """Change user password"""
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        user.password_hash = hash_password(new_password)
        
        from datetime import datetime
        user.updated_at = datetime.utcnow()
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user