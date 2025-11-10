from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List
from app.database import get_session
from app.models.user import User
from app.models.account import (
    Account, AccountType, AccountCreate, AccountUpdate,
    AccountRead, AccountDetail, AccountTree,
    AccountListResponse, AccountSummary
)
from app.core.dependencies import get_current_user
from app.services.account_service import AccountService

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new account in the chart of accounts
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    return AccountService.create_account(session, account, current_user.id)


@router.get("", response_model=AccountListResponse)
def list_accounts(
    account_type: Optional[AccountType] = Query(None, description="Filter by account type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search by code, name, or description"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get list of accounts with optional filters and pagination
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    skip = (page - 1) * page_size
    accounts, total = AccountService.get_accounts(
        session=session,
        user_id=current_user.id,
        account_type=account_type,
        is_active=is_active,
        search=search,
        skip=skip,
        limit=page_size
    )
    
    return AccountListResponse(
        total=total,
        page=page,
        page_size=page_size,
        accounts=[AccountRead.model_validate(account) for account in accounts]
    )


@router.get("/tree", response_model=List[AccountTree])
def get_account_tree(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get hierarchical account structure (tree view)
    
    Returns root accounts with nested children
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    root_accounts = AccountService.get_account_tree(session, current_user.id)
    
    def build_tree(account: Account) -> AccountTree:
        return AccountTree(
            id=account.id, # type: ignore
            code=account.code,
            name=account.name,
            type=account.type,
            balance=account.balance,
            is_active=account.is_active,
            children=[build_tree(child) for child in account.children]
        )
    
    return [build_tree(account)  for account in root_accounts]


@router.get("/summary", response_model=AccountSummary)
def get_account_summary(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get summary statistics of all accounts
    
    Shows counts and total balances by account type
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    return AccountService.get_account_summary(session, current_user.id)


@router.get("/{account_id}", response_model=AccountDetail)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get detailed information about a specific account
    
    Includes parent and children relationships
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    account = AccountService.get_account_by_id(session, account_id, current_user.id)
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return account


@router.patch("/{account_id}", response_model=AccountRead)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing account
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    return AccountService.update_account(
        session, account_id, account_update, current_user.id
    )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete an account
    
    Cannot delete accounts with:
    - Existing transactions
    - Child accounts (delete or reassign children first)
    
    **Requires authentication**
    """
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID is required"
        )
    AccountService.delete_account(session, account_id, current_user.id)
    return None