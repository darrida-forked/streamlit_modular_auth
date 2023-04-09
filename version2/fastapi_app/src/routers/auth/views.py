import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, ValidationError

from src.config import config
from src.routers.maintenance.models import DBUser

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class FastAPIUser(BaseModel):
    id: Optional[int] = None
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


################################################################################################
# AUTHENTICATION RELATED
################################################################################################
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# INITALIZE FastAPI APP
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
)


# FUNCTIONS RELATED TO AUTHENICATION
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> DBUser:
    # user = get_user(accounts(), username)
    user = DBUser.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.FASTAPI_SECRET_KEY, algorithm=config.FASTAPI_ALGORITHM)


def get_current_user_synchronous(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        logger.info(token)
        payload = jwt.decode(token, config.FASTAPI_SECRET_KEY, algorithms=[config.FASTAPI_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = DBUser.get(token_data.username)
    if user is None:
        raise credentials_exception
    logger.warning("views.py, auth, line 103")
    logger.warning(security_scopes.scopes)
    if security_scopes.scopes:
        grant = False
        for scope in security_scopes.scopes:
            if scope in token_data.scopes:
                grant = True
        if not grant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    logger.warning("views.py, uath, line 115")
    return user


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, config.FASTAPI_SECRET_KEY, algorithms=[config.FASTAPI_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = DBUser.get(token_data.username)
    if user is None:
        raise credentials_exception
    grant = False
    for scope in security_scopes.scopes:
        if scope in token_data.scopes:
            grant = True
    if not grant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return user


async def get_current_active_user(current_user: FastAPIUser = Security(get_current_user, scopes=["me"])):
    try:
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
    except AttributeError:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


##############################################################
# ENDPOINT: Authentication Token
##############################################################
def login_for_access_token_func(username, password, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=expires_minutes)
    scopes = [u.name for u in user.access]
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scopes},
        expires_delta=access_token_expires,  # pylint: disable=no-member
    )
    logger.info(f"/token auth registered: '{user.username}'; scopes={scopes}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/token",
    response_model=Token,
    tags=["Authentication"],
    responses={401: {"description": "Incorrect username or password."}},
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """## Returns Authentication Token

    **NOTE:** Information below includes fields related to scopes. These are inactive, since the setting of scope
              is being handled differently than the FastAPI boilerplate permissions (we don't need as much complexity).

    - Serves as an endpoint for an api consumer to request a temporary token for user on FastAPI endpoints
    - Token expires after 30 minutes
    - Username and password go in the request body (see section)

    ### Returns:
    - **JSON:** Returns bearer token
    """
    return login_for_access_token_func(form_data.username, form_data.password)
    # user = authenticate_user(form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # scopes = [u.name for u in user.access]
    # access_token = create_access_token(
    #     data={"sub": user.username, "scopes": scopes},
    #     expires_delta=access_token_expires,  # pylint: disable=no-member
    # )
    # logger.info(f"/token auth registered: '{user.username}'; scopes={scopes}")
    # return {"access_token": access_token, "token_type": "bearer"}
