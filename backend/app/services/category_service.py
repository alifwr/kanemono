from sqlmodel import Session, select, col
from typing import Optional
from app.models import Category, CategoryCreate, CategoryUpdate, CategoryType, User
from fastapi import HTTPException, status


class CategoryService:
    """Service for category business logic"""
    
    @staticmethod
    def create_category(
        session: Session, 
        category_data: CategoryCreate, 
        user: User
    ) -> Category:
        """Create a new category"""
        
        # Validate parent category if provided
        if category_data.parent_id:
            parent = session.get(Category, category_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found"
                )
            
            # Ensure parent belongs to the same user
            if parent.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Parent category does not belong to you"
                )
            
            # Ensure parent has the same type
            if parent.type != category_data.type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent category must have the same type (income/expense)"
                )
        
        # Check for duplicate name under the same parent
        statement = select(Category).where(
            Category.user_id == user.id,
            Category.name == category_data.name,
            Category.parent_id == category_data.parent_id
        )
        existing = session.exec(statement).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists under the same parent"
            )
        
        # Create category
        category = Category.model_validate(category_data, update={"user_id": user.id})
        session.add(category)
        session.commit()
        session.refresh(category)
        
        return category
    
    @staticmethod
    def get_categories(
        session: Session, 
        user: User,
        type: Optional[CategoryType] = None,
        parent_id: Optional[int] = None,
        include_children: bool = True
    ) -> list[Category]:
        """Get all categories for a user with optional filtering"""
        
        statement = select(Category).where(Category.user_id == user.id)
        
        # Filter by type
        if type:
            statement = statement.where(Category.type == type)
        
        # Filter by parent
        if parent_id is not None:
            statement = statement.where(Category.parent_id == parent_id)
        elif not include_children:
            # Only root categories (no parent)
            statement = statement.where(col(Category.parent_id).is_(None))
        
        statement = statement.order_by(Category.name)
        
        categories = session.exec(statement).all()
        return list(categories)
    
    @staticmethod
    def get_category(session: Session, category_id: int, user: User) -> Category:
        """Get a single category by ID"""
        
        category = session.get(Category, category_id)
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Ensure category belongs to user
        if category.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this category"
            )
        
        return category
    
    @staticmethod
    def update_category(
        session: Session, 
        category_id: int, 
        category_update: CategoryUpdate, 
        user: User
    ) -> Category:
        """Update a category"""
        
        category = CategoryService.get_category(session, category_id, user)
        
        # Validate parent if being updated
        if category_update.parent_id is not None:
            # Prevent self-reference
            if category_update.parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category cannot be its own parent"
                )
            
            # Prevent circular reference
            if CategoryService._creates_circular_reference(
                session, category_id, category_update.parent_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This would create a circular reference"
                )
            
            # Validate parent exists and belongs to user
            parent = session.get(Category, category_update.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found"
                )
            
            if parent.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Parent category does not belong to you"
                )
            
            # Ensure type compatibility
            category_type = category_update.type or category.type
            if parent.type != category_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent category must have the same type"
                )
        
        # Update fields
        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)
        
        session.add(category)
        session.commit()
        session.refresh(category)
        
        return category
    
    @staticmethod
    def delete_category(session: Session, category_id: int, user: User) -> None:
        """Delete a category"""
        
        category = CategoryService.get_category(session, category_id, user)
        
        # Check if category has children
        statement = select(Category).where(Category.parent_id == category_id)
        children = session.exec(statement).first()
        
        if children:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with subcategories. Delete children first."
            )
        
        # Check if category is used in transactions
        # Note: Uncomment when Transaction model is available
        # from app.models import Transaction
        # statement = select(Transaction).where(Transaction.category_id == category_id)
        # transactions = session.exec(statement).first()
        # if transactions:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Cannot delete category that is used in transactions"
        #     )
        
        session.delete(category)
        session.commit()
    
    @staticmethod
    def get_category_tree(
        session: Session, 
        user: User,
        type: Optional[CategoryType] = None
    ) -> list[dict]:
        """Get categories in hierarchical tree structure"""
        
        # Get all categories
        categories = CategoryService.get_categories(session, user, type=type)
        
        # Build tree structure
        category_map = {cat.id: cat for cat in categories}
        tree = []
        
        for category in categories:
            if category.parent_id is None:
                # Root category
                tree.append(CategoryService._build_tree_node(category, category_map))
        
        return tree
    
    @staticmethod
    def _build_tree_node(category: Category, category_map: dict) -> dict:
        """Recursively build tree node with children"""
        
        node = {
            "id": category.id,
            "name": category.name,
            "type": category.type,
            "icon": category.icon,
            "color": category.color,
            "parent_id": category.parent_id,
            "children": []
        }
        
        # Find children
        for cat_id, cat in category_map.items():
            if cat.parent_id == category.id:
                node["children"].append(
                    CategoryService._build_tree_node(cat, category_map)
                )
        
        return node
    
    @staticmethod
    def _creates_circular_reference(
        session: Session, 
        category_id: int, 
        new_parent_id: int
    ) -> bool:
        """Check if setting new_parent_id would create a circular reference"""
        
        current_id = new_parent_id
        max_depth = 100  # Prevent infinite loop
        depth = 0
        
        while current_id is not None and depth < max_depth:
            if current_id == category_id:
                return True  # Circular reference detected
            
            category = session.get(Category, current_id)
            if not category:
                break
            
            current_id = category.parent_id
            depth += 1
        
        return False


def create_default_categories(session: Session, user: User) -> None:
    """Create default categories for a new user"""
    
    if user.id is None:
        raise ValueError("User must have an ID to create default categories")
    
    default_categories = [
        # Income Categories
        {
            "name": "Salary",
            "type": CategoryType.INCOME,
            "icon": "💰",
            "color": "#4CAF50"
        },
        {
            "name": "Business Income",
            "type": CategoryType.INCOME,
            "icon": "💼",
            "color": "#2196F3"
        },
        {
            "name": "Investment Income",
            "type": CategoryType.INCOME,
            "icon": "📈",
            "color": "#9C27B0"
        },
        {
            "name": "Gifts Received",
            "type": CategoryType.INCOME,
            "icon": "🎁",
            "color": "#E91E63"
        },
        {
            "name": "Other Income",
            "type": CategoryType.INCOME,
            "icon": "💵",
            "color": "#00BCD4"
        },
        
        # Expense Categories - Parents
        {
            "name": "Food & Dining",
            "type": CategoryType.EXPENSE,
            "icon": "🍔",
            "color": "#FF5722",
            "children": [
                {"name": "Groceries", "icon": "🛒", "color": "#FF5722"},
                {"name": "Restaurants", "icon": "🍽️", "color": "#FF5722"},
                {"name": "Coffee Shops", "icon": "☕", "color": "#FF5722"}
            ]
        },
        {
            "name": "Housing",
            "type": CategoryType.EXPENSE,
            "icon": "🏠",
            "color": "#795548",
            "children": [
                {"name": "Rent", "icon": "🏘️", "color": "#795548"},
                {"name": "Utilities", "icon": "💡", "color": "#795548"},
                {"name": "Home Maintenance", "icon": "🔧", "color": "#795548"}
            ]
        },
        {
            "name": "Transportation",
            "type": CategoryType.EXPENSE,
            "icon": "🚗",
            "color": "#607D8B",
            "children": [
                {"name": "Gas", "icon": "⛽", "color": "#607D8B"},
                {"name": "Public Transit", "icon": "🚌", "color": "#607D8B"},
                {"name": "Car Maintenance", "icon": "🔧", "color": "#607D8B"}
            ]
        },
        {
            "name": "Shopping",
            "type": CategoryType.EXPENSE,
            "icon": "🛍️",
            "color": "#E91E63",
            "children": [
                {"name": "Clothing", "icon": "👕", "color": "#E91E63"},
                {"name": "Electronics", "icon": "💻", "color": "#E91E63"},
                {"name": "Personal Care", "icon": "💄", "color": "#E91E63"}
            ]
        },
        {
            "name": "Entertainment",
            "type": CategoryType.EXPENSE,
            "icon": "🎮",
            "color": "#9C27B0",
            "children": [
                {"name": "Movies", "icon": "🎬", "color": "#9C27B0"},
                {"name": "Games", "icon": "🎮", "color": "#9C27B0"},
                {"name": "Hobbies", "icon": "🎨", "color": "#9C27B0"}
            ]
        },
        {
            "name": "Healthcare",
            "type": CategoryType.EXPENSE,
            "icon": "🏥",
            "color": "#F44336",
            "children": [
                {"name": "Doctor", "icon": "👨‍⚕️", "color": "#F44336"},
                {"name": "Pharmacy", "icon": "💊", "color": "#F44336"},
                {"name": "Insurance", "icon": "🛡️", "color": "#F44336"}
            ]
        },
        {
            "name": "Other Expenses",
            "type": CategoryType.EXPENSE,
            "icon": "📦",
            "color": "#9E9E9E"
        }
    ]
    
    # Create categories
    for cat_data in default_categories:
        children_data = cat_data.pop("children", [])
        
        # Create parent category
        parent_category = Category(
            user_id=user.id,
            name=cat_data["name"],
            type=cat_data["type"],
            icon=cat_data.get("icon"),
            color=cat_data.get("color")
        )
        session.add(parent_category)
        session.flush()  # Get the ID without committing
        
        # Create children categories
        for child_data in children_data:
            child_category = Category(
                user_id=user.id,
                parent_id=parent_category.id,
                name=child_data["name"],
                type=cat_data["type"],
                icon=child_data.get("icon"),
                color=child_data.get("color")
            )
            session.add(child_category)
    
    session.commit()