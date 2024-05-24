from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from models.schemas.jwt_schema import JWTUser

ALGORITHM = 'HS256'
JWT_TOKEN_EXPIRE_MINUTES = timedelta(minutes=10)
SECRET_KEY = '1213265115156132165156156155653156'

def create_jwt_token(
        *,
        jwt_content: Dict[str, str],
        secret_key: str,
        expires_detal: timedelta,
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_detal
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt.decode("utf-8")

def create_access_token_user(user) -> str:
    return create_jwt_token(
        jwt_content={**JWTUser(sub=user.login, role=user.role).dict()},
        secret_key=SECRET_KEY,
        expires_detal=JWT_TOKEN_EXPIRE_MINUTES,
    )

def get_user_role(token) -> str:
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    try:
        return jwt.decode(token,
                          SECRET_KEY,
                          algorithms=[ALGORITHM],
                          options={'verify_signature': False}
                          )['role']
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT Token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in Token") from validation_error