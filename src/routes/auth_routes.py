from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel
from typing import Dict, Optional
from src.database.database import Database
from src.utils.auth import create_access_token, get_current_user
from src.config import settings
import hashlib

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}},
)

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    is_active: bool

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hashed version
    
    In a real application, use a secure password hashing library like bcrypt or Argon2
    """
    # This is a simple example - use a proper password hashing library in production
    password_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    print(f"Comparing passwords: {password_hash} == {hashed_password}")
    return password_hash == hashed_password

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256
    
    In a real application, use a secure password hashing library like bcrypt or Argon2
    """
    return hashlib.sha256(password.encode()).hexdigest()

async def authenticate_user(db: Database, username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user by username and password
    """
    try:
        print(f"Authenticating user: {username}")
        # Get the users collection
        users_collection = await db.get_collection("users")
        print(f"Got users collection")
        
        # Find user by username
        user = await users_collection.find_one({"username": username})
        print(f"User lookup result: {user is not None}")
        
        if not user:
            print(f"User {username} not found")
            return None
        
        if not verify_password(password, user["password"]):
            print(f"Password verification failed for {username}")
            return None
        
        print(f"Authentication successful for {username}")
        return user
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return None

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate
):
    """
    Register a new user
    
    This is for testing purposes and should have more validation in production
    """
    try:
        db = Database.get_instance()
        users_collection = await db.get_collection("users")
        
        # Check if username already exists
        existing_user = await users_collection.find_one({"username": user_data.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Find the maximum user_id and increment by 1
        latest_user = await users_collection.find_one(
            {}, 
            sort=[("user_id", -1)]
        )
        
        new_user_id = 10001
        if latest_user and "user_id" in latest_user:
            new_user_id = latest_user["user_id"] + 1
        
        # Create new user document
        new_user = {
            "user_id": new_user_id,
            "username": user_data.username,
            "email": user_data.email,
            "password": hash_password(user_data.password),
            "role": user_data.role,
            "is_active": True
        }
        
        # Insert into database
        await users_collection.insert_one(new_user)
        
        # Remove password from response
        new_user.pop("password")
        
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticate user and provide JWT token
    
    This endpoint is used for OAuth2 password flow authentication.
    It validates the username and password, then returns a JWT token.
    """
    print(f"OAuth2 login attempt: {form_data.username}")
    db = Database.get_instance()
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        print(f"User account is disabled: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user data
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={
            "sub": user["user_id"],
            "role": user.get("role", "user")
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user.get("role", "user")
    }

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin
):
    """
    Authenticate user with username and password
    
    This endpoint provides a more standard login interface, accepting
    username and password in the request body.
    """
    print(f"JSON login attempt: {user_data.username}")
    db = Database.get_instance()
    user = await authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        print(f"User account is disabled: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    # Create access token with user data
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={
            "sub": user["user_id"],
            "role": user.get("role", "user")
        },
        expires_delta=access_token_expires
    )
    
    print(f"Login successful: {user_data.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user.get("role", "user")
    }