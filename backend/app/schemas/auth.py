from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


# Registration
class RegisterRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)  # Added max_length
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        """Optional: Add password strength validation"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


# Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)  # Added max_length


# Change Password
class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password')
    def validate_password_strength(cls, v):
        """Optional: Add password strength validation"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


# Reset Password
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password')
    def validate_password_strength(cls, v):
        """Optional: Add password strength validation"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


class RegisterResponse(BaseModel):
    id: int
    email: str
    name: str
    message: str = "User registered successfully"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordResponse(BaseModel):
    message: str = "Password reset successfully"


class ChangePasswordResponse(BaseModel):
    message: str = "Password changed successfully"


class UserProfile(BaseModel):
    id: int
    email: str
    name: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None