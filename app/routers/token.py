import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt
from pydantic import Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SECRET_KEY = "a9646c30a5a8a493c375ff549bbc603660e03c9d057d72f249f264fb4a07c832"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Note: In actual production, we will store root user in a database
ROOT_USERS_DB = {
    "root": {
        "username": "root",
        "hashed_password": '$2b$12$/eLylqVxNCF0YkuQhAs5eeGJGonPi2FJpSCj.dq4C1zG8IJKSmyCW',
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str = Field(
        ...,
        description="Username",
        example="Peter"
    )


class UserInDB(User):
    hashed_password: str


class UserGen(User):
    expire_days: float = Field(
        ...,
        description="Number of days till token expire",
        example=360.0,
    )


router = APIRouter(
    prefix="/token",
    tags=["token"],
    responses={401: {"description": "Unauthorized"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash
    """
    return pwd_context.hash(password)


def get_user(db, username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(user_db, username: str, password: str) -> Optional[UserInDB]:
    user = get_user(user_db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post(
    "/",
    response_model=Token,
    description=f"Log in as root user to get root token (valid for {ACCESS_TOKEN_EXPIRE_MINUTES} minutes)"
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        ROOT_USERS_DB, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_root_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logger.info(f"JWT error. Error: {e}")
        raise credentials_exception

    user = get_user(ROOT_USERS_DB, username)
    if user is None:
        raise credentials_exception

    return user


async def get_regular_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logger.info(f"JWT error. Error: {e}")
        raise credentials_exception

    return User(username=username)


@router.put(
    "/generate",
    response_model=Token,
    description="Generate user token. Require root JWT authorization token."
)
async def generate_token(
    user_gen: UserGen,
    user: UserInDB = Depends(get_root_user)
):
    """Generaate user token

    Note:
        - In real application, once we generate a token for a user, we should
          save it in a database.
        - However, here we just return the token. This is the case where you
          don't need to perform user management (such as revoke user access).

    """
    logger.info(
        f"{user.username} creates a {user_gen.expire_days} days token for {user_gen.username}"
    )
    access_token_expires = timedelta(days=user_gen.expire_days)
    access_token = create_access_token(
        data={"sub": user_gen.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/root-test",
    response_model=User,
    description="Test root user access. Require root JWT authorization token."
)
async def test_root_api(user: UserInDB = Depends(get_root_user)):
    return user


@router.get(
    "/reg-test",
    response_model=User,
    description="Test regular user access. Require user JWT authorization token."
)
async def test_regular_user_api(user: User = Depends(get_regular_user)):
    return user
