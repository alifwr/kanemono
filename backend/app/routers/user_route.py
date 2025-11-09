from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from sqlmodel import select

from app.services.database import SessionDep
from app.models.user_model import User, UserCreate

router = APIRouter()

@router.get("/users/")
async def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    try:
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        return list(users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")


@router.post("/users/")
async def create_user(user: UserCreate, session: SessionDep) -> User:
    try:
        db_user = User(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@router.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> User:
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        # Re-raise HTTPException (like 404) without wrapping
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}
    except HTTPException:
        # Re-raise HTTPException (like 404) without wrapping
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")