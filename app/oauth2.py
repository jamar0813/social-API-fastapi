from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, oauth2
from sqlalchemy.orm import Session
from .config import settings

# Pass users creditials through
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret Key
SECRET_KEY = f'{settings.secret_key}'
# algorithm
ALGORITHM = f'{settings.algorithm}'
# expiration Time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Create the JWT token definition
def create_access_token(data: dict):
    #Make a copy of the data payload
    to_encode = data.copy()

    #create time from login to token expiration
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    #creat JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

# Verify that the JWT token is valid with proper secret
def verify_access_token(token: str, creditentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise creditentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise creditentials_exception

    return token_data

# Decode JWT and get user id
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= f'Could not validate credentials',
        headers= {
            "WWW-Authenicate": "Bearer"
        }
    )

    # Parse the id form token then fetch user from database
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user