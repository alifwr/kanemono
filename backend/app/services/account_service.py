from sqlmodel import Session, select, or_, func
from fastapi import HTTPException, status
from typing import Optional, List
from decimal import Decimal
from app.models.account import Account, AccountType, AccountCreate, AccountUpdate


class AccountService:
    """Service layer for account operations"""
    
    @staticmethod
    def get_account_by_id(session: Session, account_id: int, user_id: int) -> Optional[Account]:
        """Get account by ID for specific user"""
        statement = select(Account).where(
            Account.id == account_id,
            Account.user_id == user_id
        )
        return session.exec(statement).first()
    
    @staticmethod
    def get_account_by_code(session: Session, code: str, user_id: int) -> Optional[Account]:
        """Get account by code for specific user"""
        statement = select(Account).where(
            Account.code == code,
            Account.user_id == user_id
        )
        return session.exec(statement).first()
    
    @staticmethod
    def create_account(
        session: Session,
        account_data: AccountCreate,  # ✅ Added proper type hint
        user_id: int
    ) -> Account:
        """Create a new account"""
        # Check if code already exists
        existing = AccountService.get_account_by_code(session, account_data.code, user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Account code '{account_data.code}' already exists"
            )
        
        # Validate parent account if provided
        if account_data.parent_id:
            parent = AccountService.get_account_by_id(session, account_data.parent_id, user_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent account not found"
                )
        
        # Create account
        account = Account(
            user_id=user_id,
            code=account_data.code,
            name=account_data.name,
            type=account_data.type,
            subtype=account_data.subtype,
            normal_balance=account_data.normal_balance,
            description=account_data.description,
            is_active=account_data.is_active,
            parent_id=account_data.parent_id
        )
        
        session.add(account)
        session.commit()
        session.refresh(account)
        
        return account
    
    @staticmethod
    def update_account(
        session: Session,
        account_id: int,
        account_data: AccountUpdate,  # ✅ Added proper type hint
        user_id: int
    ) -> Account:
        """Update an existing account"""
        account = AccountService.get_account_by_id(session, account_id, user_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Check if new code conflicts with existing
        if account_data.code and account_data.code != account.code:
            existing = AccountService.get_account_by_code(session, account_data.code, user_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Account code '{account_data.code}' already exists"
                )
        
        # Validate parent account if changed
        if account_data.parent_id is not None and account_data.parent_id != account.parent_id:
            # Prevent circular reference
            if account_data.parent_id == account.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account cannot be its own parent"
                )
            
            parent = AccountService.get_account_by_id(session, account_data.parent_id, user_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent account not found"
                )
        
        # Update fields
        update_data = account_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(account, field, value)
        
        from datetime import datetime
        account.updated_at = datetime.utcnow()
        
        session.add(account)
        session.commit()
        session.refresh(account)
        
        return account
    
    @staticmethod
    def delete_account(session: Session, account_id: int, user_id: int) -> bool:
        """Delete an account"""
        account = AccountService.get_account_by_id(session, account_id, user_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Check if account has children
        statement = select(Account).where(Account.parent_id == account_id)
        children = session.exec(statement).first()
        if children:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete account with child accounts. Delete or reassign children first."
            )
        
        # TODO: Check if account has transactions when transaction model is implemented
        # if account.transaction_lines:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Cannot delete account with existing transactions"
        #     )
        
        session.delete(account)
        session.commit()
        
        return True
    
    @staticmethod
    def get_accounts(
        session: Session,
        user_id: int,
        account_type: Optional[AccountType] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Account], int]:
        """Get list of accounts with filters"""
        # Build query
        statement = select(Account).where(Account.user_id == user_id)
        
        # Apply filters
        if account_type:
            statement = statement.where(Account.type == account_type)
        
        if is_active is not None:
            statement = statement.where(Account.is_active == is_active)
        
        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                or_(
                    Account.code.ilike(search_term),  # type: ignore
                    Account.name.ilike(search_term),  # type: ignore
                    Account.description.ilike(search_term)  # type: ignore
                )
            )
        
        # Get total count
        count_statement = select(func.count()).select_from(statement.subquery())
        total = session.exec(count_statement).one()
        
        # Apply pagination and ordering
        statement = statement.offset(skip).limit(limit).order_by(Account.code)
        
        accounts = session.exec(statement).all()
        
        return list(accounts), total
    
    @staticmethod
    def get_account_tree(session: Session, user_id: int) -> List[Account]:
        """Get hierarchical account structure (root accounts only)"""
        statement = select(Account).where(
            Account.user_id == user_id,
            Account.parent_id == None  # ✅ Changed from == None to is None
        ).order_by(Account.code)
        
        return list(session.exec(statement).all())
    
    @staticmethod
    def get_account_summary(session: Session, user_id: int) -> dict:
        """Get account summary statistics"""
        # Count by type
        statement = select(
            Account.type,
            func.count().label('count'),
            func.sum(Account.balance).label('total_balance')
        ).where(
            Account.user_id == user_id
        ).group_by(Account.type)
        
        results = session.exec(statement).all()
        
        summary = {
            "total_accounts": 0,
            "assets_count": 0,
            "liabilities_count": 0,
            "equity_count": 0,
            "revenue_count": 0,
            "expense_count": 0,
            "total_assets": Decimal("0.00"),
            "total_liabilities": Decimal("0.00"),
            "total_equity": Decimal("0.00"),
            "total_revenue": Decimal("0.00"),
            "total_expenses": Decimal("0.00")
        }
        
        for row in results:
            account_type, count, balance = row
            balance = balance or Decimal("0.00")
            
            summary["total_accounts"] += count
            
            if account_type == AccountType.ASSET:
                summary["assets_count"] = count
                summary["total_assets"] = balance
            elif account_type == AccountType.LIABILITY:
                summary["liabilities_count"] = count
                summary["total_liabilities"] = balance
            elif account_type == AccountType.EQUITY:
                summary["equity_count"] = count
                summary["total_equity"] = balance
            elif account_type == AccountType.REVENUE:
                summary["revenue_count"] = count
                summary["total_revenue"] = balance
            elif account_type == AccountType.EXPENSE:
                summary["expense_count"] = count
                summary["total_expenses"] = balance
        
        return summary