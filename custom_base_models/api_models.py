from pydantic import BaseModel


class Token(BaseModel):
    """
    Model de resposta do token de acesso.
    """
    access_token: str
    token_type: str


class PasswordChangeRequest(BaseModel):
    """
    Model de requisição para alteração de senha.
    """
    username: str
    new_password: str
    application_token: str


class QueryUserRequest(BaseModel):
    """
    Model de requisição para consulta de usuário.
    """
    username: str
    application_token: str


class LoginRequest(BaseModel):
    """
    Model de requisição de login.
    """
    username: str
    password: str
