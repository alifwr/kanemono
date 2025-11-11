from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from typing import Optional

from app.models import (
    Category, 
    CategoryCreate, 
    CategoryRead, 
    CategoryUpdate,
    CategoryType,
    User
)
from app.services.category_service import CategoryService
from app.core.dependencies import get_session, get_current_user

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category"
)
def create_category(
    category_data: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new category for the current user.
    
    - **name**: Category name (required)
    - **type**: income or expense (required)
    - **parent_id**: Parent category ID for subcategories (optional)
    - **icon**: Icon/emoji for UI (optional)
    - **color**: Hex color code (optional)
    """
    return CategoryService.create_category(session, category_data, current_user)


@router.get(
    "/",
    response_model=list[CategoryRead],
    summary="Get all categories"
)
def get_categories(
    type: Optional[CategoryType] = Query(None, description="Filter by type (income/expense)"),
    parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
    include_children: bool = Query(True, description="Include child categories"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all categories for the current user.
    
    Query parameters:
    - **type**: Filter by income or expense
    - **parent_id**: Get categories under a specific parent (null = root only)
    - **include_children**: Include subcategories in results
    """
    return CategoryService.get_categories(
        session, 
        current_user, 
        type=type,
        parent_id=parent_id,
        include_children=include_children
    )


@router.get(
    "/tree",
    response_model=list[dict],
    summary="Get categories in tree structure"
)
def get_category_tree(
    type: Optional[CategoryType] = Query(None, description="Filter by type"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get categories organized in a hierarchical tree structure.
    
    Returns nested JSON with parent-child relationships.
    """
    return CategoryService.get_category_tree(session, current_user, type=type)


@router.get(
    "/by-type/{type}",
    response_model=list[CategoryRead],
    summary="Get categories by type"
)
def get_categories_by_type(
    type: CategoryType,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all categories filtered by type (income or expense).
    """
    return CategoryService.get_categories(session, current_user, type=type)


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Get a single category"
)
def get_category(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific category by ID.
    """
    return CategoryService.get_category(session, category_id, current_user)


@router.patch(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Update a category"
)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a category.
    
    All fields are optional. Only provided fields will be updated.
    """
    return CategoryService.update_category(
        session, 
        category_id, 
        category_update, 
        current_user
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category"
)
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a category.
    
    Note: Cannot delete categories that have:
    - Subcategories (delete children first)
    - Associated transactions
    """
    CategoryService.delete_category(session, category_id, current_user)
    return None