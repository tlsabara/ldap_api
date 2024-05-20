import socket
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

from api_functions import create_access_token, decode_access_token
from base.ldap_utils import get_user_dn, authenticate_ldap_user, get_my_ldap_info, change_user_password, get_all_items
from configs import SERVER_TOKEN
from custom_base_models.api_models import Token, PasswordChangeRequest, QueryUserRequest, LoginRequest

app = FastAPI()

@app.get("/")
@app.post("/")
async def root():
    """
    Retorna uma mensagem de boas-vindas.

    Returns:
        dict: Mensagem de boas-vindas.
    """
    return {"running": True}

@app.get("/healthcheck")
async def healthcheck():
    """
    Verifica a integridade do servidor LDAP.

    Returns:
        dict: Status da integridade do servidor LDAP.
    """
    return {
        "host_check": socket.gethostbyname(socket.gethostname()),
        "ldap_check": "error" if get_all_items() == [] else "ok",
    }

@app.post("/login", response_model=Token)
async def login(form_data: LoginRequest):
    """
    Realiza o login do usuário.

    Args:
        form_data (LoginRequest): Dados de login do usuário.

    Returns:
        dict: O token de acesso JWT e o tipo de token.

    Raises:
        HTTPException: Se as credenciais forem inválidas.
    """
    username = form_data.username
    password = form_data.password

    if not authenticate_ldap_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user_exists/")
async def user_exists(request: QueryUserRequest):
    """
    Verifica se um usuário existe no servidor LDAP.

    Args:
        request (QueryUserRequest): Requisição contendo o token da aplicação e o nome de usuário.

    Returns:
        dict: Um dicionário indicando se o usuário existe.

    Raises:
        HTTPException: Se o token da aplicação for inválido.
    """
    if request.application_token != SERVER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid server token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_dn = get_user_dn(request.username)
    if user_dn:
        return {"exists": True}
    else:
        return {"exists": False}


@app.post("/change_password")
async def change_password(request: PasswordChangeRequest):
    """
    Altera a senha de um usuário no servidor LDAP.

    Args:
        request (PasswordChangeRequest): Requisição contendo o token da aplicação, nome de usuário e nova senha.

    Returns:
        dict: Uma mensagem indicando o sucesso da operação.

    Raises:
        HTTPException: Se o token da aplicação for inválido, o usuário não for encontrado ou ocorrer um erro ao alterar a senha.
    """
    if request.application_token != SERVER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid server token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_dn = get_user_dn(request.username)
    if not user_dn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not change_user_password(user_dn, request.new_password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password on LDAP server",
        )

    return {"message": "Password changed successfully"}


@app.get("/myinfo")
async def myinfo(username: Annotated[str, Depends(decode_access_token)]):
    """
    Retorna as informações do usuário a partir do servidor LDAP.

    Args:
        username (Annotated[str, Depends(decode_access_token)]): Nome de usuário decodificado do token JWT.

    Returns:
        dict: Informações do usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado ou ocorrer um erro ao obter as informações.
    """
    user_dn = get_user_dn(username)
    if not user_dn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = get_my_ldap_info(user_dn)
    if result:
        user_info = result[0][1]
        return user_info
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User information not found",
        )
