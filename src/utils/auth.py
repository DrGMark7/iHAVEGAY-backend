from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from pydantic import BaseModel
from src.config import settings
from src.database.database import Database

# OAuth2 scheme for token authentication - Use relative path without API prefix
# This will be combined with the API prefix automatically
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Model for JWT token data
class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None
    exp: Optional[datetime] = None

async def get_user_by_id(db: Database, user_id: int) -> Dict:
    """
    Get user information from database by user ID
    """
    try:
        # Get the users collection
        users_collection = await db.get_collection("users")
        # Find user by user_id
        user = await users_collection.find_one({"user_id": user_id})
        print(f"User lookup result for ID {user_id}: {user is not None}")
        if not user:
            return None
        return user
    except Exception as e:
        print(f"Error in get_user_by_id: {str(e)}")
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Validate the JWT token and return the current user's information
    
    This function is used as a dependency in routes that require authentication.
    It verifies the JWT token, extracts the user ID, and fetches the user data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        print(f"Received token: {token[:10]}...")
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        print(f"Token payload: {payload}")
        
        # Extract user ID from payload - convert to int if it's a string
        user_id_str = payload.get("sub")
        if user_id_str is None:
            print("No 'sub' field in token payload")
            raise credentials_exception
        
        # Convert user_id to integer if it's a string
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            print(f"Invalid user_id format: {user_id_str}")
            raise credentials_exception
        
        # Create token data
        token_data = TokenData(
            user_id=user_id,
            role=payload.get("role", "user"),
            exp=datetime.fromtimestamp(payload.get("exp", 0))
        )
        
        # Check if token has expired
        if token_data.exp < datetime.now():
            print(f"Token has expired: {token_data.exp} < {datetime.now()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    except JWTError as e:
        print(f"JWT error: {str(e)}")
        raise credentials_exception
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        raise credentials_exception
    
    # Get the database instance
    db = Database.get_instance()
    
    # Get user from database
    user = await get_user_by_id(db, token_data.user_id)
    if user is None:
        print(f"User with ID {token_data.user_id} not found in database")
        raise credentials_exception
    
    # Add role to user data if not present
    if "role" not in user:
        user["role"] = token_data.role
    
    return user

async def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Convert user_id to string for JWT compatibility
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])
    
    to_encode.update({"exp": expire.timestamp()})
    print(f"Creating token with payload: {to_encode}")
    
    # Create JWT token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

# Helper function for testing purposes - returns a mocked user
# Should be removed in production
async def get_current_user_mock() -> Dict:
    """
    Mock function for testing without actual JWT token
    This should be removed in production
    """
    return {
        "user_id": 10001,
        "username": "testuser",
        "email": "test@example.com",
        "role": "admin",
        "is_active": True
    }
