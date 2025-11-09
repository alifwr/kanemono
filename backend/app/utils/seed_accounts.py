from sqlmodel import Session
from app.models.account import Account, AccountType, NormalBalance
from app.models.user import User


def create_default_accounts(session: Session, user_id: int):
    """
    Create default chart of accounts for a new user
    Standard accounting structure
    """
    default_accounts = [
        # ASSETS (1000-1999)
        {
            "code": "1000",
            "name": "Assets",
            "type": AccountType.ASSET,
            "subtype": "Group",
            "normal_balance": NormalBalance.DEBIT,
            "description": "All asset accounts",
            "parent_code": None
        },
        {
            "code": "1100",
            "name": "Current Assets",
            "type": AccountType.ASSET,
            "subtype": "Group",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Short-term assets",
            "parent_code": "1000"
        },
        {
            "code": "1110",
            "name": "Cash",
            "type": AccountType.ASSET,
            "subtype": "Current Asset",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Cash on hand",
            "parent_code": "1100"
        },
        {
            "code": "1120",
            "name": "Bank Account",
            "type": AccountType.ASSET,
            "subtype": "Current Asset",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Main bank account",
            "parent_code": "1100"
        },
        {
            "code": "1130",
            "name": "Savings Account",
            "type": AccountType.ASSET,
            "subtype": "Current Asset",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Savings account",
            "parent_code": "1100"
        },
        
        # LIABILITIES (2000-2999)
        {
            "code": "2000",
            "name": "Liabilities",
            "type": AccountType.LIABILITY,
            "subtype": "Group",
            "normal_balance": NormalBalance.CREDIT,
            "description": "All liability accounts",
            "parent_code": None
        },
        {
            "code": "2100",
            "name": "Current Liabilities",
            "type": AccountType.LIABILITY,
            "subtype": "Group",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Short-term liabilities",
            "parent_code": "2000"
        },
        {
            "code": "2110",
            "name": "Credit Card",
            "type": AccountType.LIABILITY,
            "subtype": "Current Liability",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Credit card balance",
            "parent_code": "2100"
        },
        {
            "code": "2120",
            "name": "Loans Payable",
            "type": AccountType.LIABILITY,
            "subtype": "Current Liability",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Short-term loans",
            "parent_code": "2100"
        },
        
        # EQUITY (3000-3999)
        {
            "code": "3000",
            "name": "Equity",
            "type": AccountType.EQUITY,
            "subtype": "Group",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Owner's equity",
            "parent_code": None
        },
        {
            "code": "3100",
            "name": "Owner's Capital",
            "type": AccountType.EQUITY,
            "subtype": "Capital",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Initial capital investment",
            "parent_code": "3000"
        },
        
        # REVENUE (4000-4999)
        {
            "code": "4000",
            "name": "Revenue",
            "type": AccountType.REVENUE,
            "subtype": "Group",
            "normal_balance": NormalBalance.CREDIT,
            "description": "All income accounts",
            "parent_code": None
        },
        {
            "code": "4100",
            "name": "Salary Income",
            "type": AccountType.REVENUE,
            "subtype": "Operating Income",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Monthly salary",
            "parent_code": "4000"
        },
        {
            "code": "4200",
            "name": "Business Income",
            "type": AccountType.REVENUE,
            "subtype": "Operating Income",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Business revenue",
            "parent_code": "4000"
        },
        {
            "code": "4300",
            "name": "Investment Income",
            "type": AccountType.REVENUE,
            "subtype": "Non-Operating Income",
            "normal_balance": NormalBalance.CREDIT,
            "description": "Dividends, interest",
            "parent_code": "4000"
        },
        
        # EXPENSES (5000-5999)
        {
            "code": "5000",
            "name": "Expenses",
            "type": AccountType.EXPENSE,
            "subtype": "Group",
            "normal_balance": NormalBalance.DEBIT,
            "description": "All expense accounts",
            "parent_code": None
        },
        {
            "code": "5100",
            "name": "Housing Expenses",
            "type": AccountType.EXPENSE,
            "subtype": "Group",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Housing related expenses",
            "parent_code": "5000"
        },
        {
            "code": "5110",
            "name": "Rent",
            "type": AccountType.EXPENSE,
            "subtype": "Housing",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Monthly rent payment",
            "parent_code": "5100"
        },
        {
            "code": "5120",
            "name": "Utilities",
            "type": AccountType.EXPENSE,
            "subtype": "Housing",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Electricity, water, gas",
            "parent_code": "5100"
        },
        {
            "code": "5200",
            "name": "Food Expenses",
            "type": AccountType.EXPENSE,
            "subtype": "Group",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Food related expenses",
            "parent_code": "5000"
        },
        {
            "code": "5210",
            "name": "Groceries",
            "type": AccountType.EXPENSE,
            "subtype": "Food",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Grocery shopping",
            "parent_code": "5200"
        },
        {
            "code": "5220",
            "name": "Dining Out",
            "type": AccountType.EXPENSE,
            "subtype": "Food",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Restaurants, cafes",
            "parent_code": "5200"
        },
        {
            "code": "5300",
            "name": "Transportation",
            "type": AccountType.EXPENSE,
            "subtype": "Group",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Transportation expenses",
            "parent_code": "5000"
        },
        {
            "code": "5310",
            "name": "Fuel",
            "type": AccountType.EXPENSE,
            "subtype": "Transportation",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Vehicle fuel",
            "parent_code": "5300"
        },
        {
            "code": "5320",
            "name": "Public Transit",
            "type": AccountType.EXPENSE,
            "subtype": "Transportation",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Bus, train, taxi",
            "parent_code": "5300"
        },
        {
            "code": "5400",
            "name": "Entertainment",
            "type": AccountType.EXPENSE,
            "subtype": "Operating Expense",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Entertainment and leisure",
            "parent_code": "5000"
        },
        {
            "code": "5500",
            "name": "Healthcare",
            "type": AccountType.EXPENSE,
            "subtype": "Operating Expense",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Medical expenses",
            "parent_code": "5000"
        },
        {
            "code": "5600",
            "name": "Education",
            "type": AccountType.EXPENSE,
            "subtype": "Operating Expense",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Education and training",
            "parent_code": "5000"
        },
        {
            "code": "5700",
            "name": "Shopping",
            "type": AccountType.EXPENSE,
            "subtype": "Operating Expense",
            "normal_balance": NormalBalance.DEBIT,
            "description": "General shopping",
            "parent_code": "5000"
        },
        {
            "code": "5800",
            "name": "Insurance",
            "type": AccountType.EXPENSE,
            "subtype": "Operating Expense",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Insurance premiums",
            "parent_code": "5000"
        },
        {
            "code": "5900",
            "name": "Other Expenses",
            "type": AccountType.EXPENSE,
            "subtype": "Operating Expense",
            "normal_balance": NormalBalance.DEBIT,
            "description": "Miscellaneous expenses",
            "parent_code": "5000"
        }
    ]
    
    # Create accounts in two passes to handle parent-child relationships
    # Pass 1: Create all accounts without parent relationships
    account_map = {}  # Map code to account ID
    
    for acc_data in default_accounts:
        account = Account(
            user_id=user_id,
            code=acc_data["code"],
            name=acc_data["name"],
            type=acc_data["type"],
            subtype=acc_data["subtype"],
            normal_balance=acc_data["normal_balance"],
            description=acc_data["description"]
        )
        session.add(account)
        session.flush()  # Get ID without committing
        account_map[acc_data["code"]] = account.id
    
    # Pass 2: Update parent relationships
    for acc_data in default_accounts:
        if acc_data["parent_code"]:
            account_code = acc_data["code"]
            parent_code = acc_data["parent_code"]
            
            # Find the account and update its parent_id
            from sqlmodel import select
            statement = select(Account).where(
                Account.user_id == user_id,
                Account.code == account_code
            )
            account = session.exec(statement).first()
            
            if account and parent_code in account_map:
                account.parent_id = account_map[parent_code]
                session.add(account)
    
    # Commit all changes
    session.commit()
    print(f"✅ Created {len(default_accounts)} default accounts for user {user_id}")