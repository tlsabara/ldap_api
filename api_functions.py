import datetime as datetime_base
from datetime import timedelta, datetime
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from starlette import status

from configs import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


get_bearer_token = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))) -> str:
    """
    Cria um token de acesso JWT.

    Args:
        data (dict): Dados a serem incluídos no token.
        expires_delta (timedelta, optional): Tempo de expiração do token. O padrão é 30 minutos.

    Returns:
        str: O token de acesso JWT.
    """
    to_encode = data.copy()
    expire = datetime.now(datetime_base.UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)) -> str:
    """
    Decodifica um token de acesso JWT.

    Args:
        auth (Optional[HTTPAuthorizationCredentials], optional): Credenciais de autenticação HTTP. O padrão é None.

    Returns:
        str: O nome de usuário extraído do token.

    Raises:
        HTTPException: Se o token for inválido ou não puder ser validado.
    """
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid server token"
        )
    try:
        token = auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
