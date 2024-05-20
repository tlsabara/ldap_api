import ldap
from configs import LDAP_SERVER, LDAP_USER_DN, LDAP_USER_PASSWORD, LDAP_BASE_DN

def get_all_items() -> list:
    """
    Busca todos os itens no servidor LDAP.

    Args:
        base_dn (str): O DN (Distinguished Name) da base de dados.

    Returns:
        list: A lista de todos os itens da base de dados.
    """
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(LDAP_USER_DN, LDAP_USER_PASSWORD)
        result = conn.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, '(objectClass=*)')
        return result
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return []


def get_user_dn(username: str) -> str | None:
    """
    Obtém o DN (Distinguished Name) de um usuário no servidor LDAP.

    Args:
        username (str): O nome de usuário a ser pesquisado.

    Returns:
        str: O DN do usuário, se encontrado. Caso contrário, retorna None.
    """
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(LDAP_USER_DN, LDAP_USER_PASSWORD)
        search_filter = f"(uid={username})"
        result = conn.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, search_filter)
        if result:
            return result[0][0]
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return None


def authenticate_ldap_user(username: str, password: str) -> bool:
    """
    Autentica um usuário no servidor LDAP.

    Args:
        username (str): O nome de usuário a ser autenticado.
        password (str): A senha do usuário.

    Returns:
        bool: True se a autenticação for bem-sucedida, False caso contrário.
    """
    user_dn = get_user_dn(username)
    if not user_dn:
        return False
    conn = ldap.initialize(LDAP_SERVER)
    try:
        conn.simple_bind_s(user_dn, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return False


def get_my_ldap_info(username: str) -> list:
    """
    Retorna as informações de um usuário no servidor LDAP.

    Args:
        username (str): O nome de usuário a ser pesquisado.

    Returns:
        list: Uma lista contendo as informações do usuário, se encontrado. Caso contrário, retorna uma lista vazia.
    """
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(LDAP_USER_DN, LDAP_USER_PASSWORD)
        search_filter = f"(uid={username})"
        result = conn.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, search_filter)
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return []
    return result


def change_user_password(user_dn: str, new_password: str) -> bool:
    """
    Altera a senha de um usuário no servidor LDAP.

    Args:
        user_dn (str): O DN (Distinguished Name) do usuário a ser alterado.
        new_password (str): A nova senha do usuário.

    Returns:
        bool: True se a alteração for bem-sucedida, False caso contrário.
    """
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(LDAP_USER_DN, LDAP_USER_PASSWORD)
        conn.passwd_s(user_dn, None, new_password)
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return False
    return True
