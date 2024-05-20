# LDAP API
Uma simples api para autenticação LDAP.

Este servidor conecta no seu ldap e realiza operações de autenticação e gerenciamento de usuário básicas.
- Consulta do usuário
- Validação de autenticação com o ldap
- Troca de senha do usuário

Após a autenticação, o servidor retorna um token para o usuário poder consultar os dados.
Pra troca de senha do usuário do AD o Frontend deve utilizar o SERVER_TOKEN para poder realizar a operacão.

### Configuração inicial

ajustes no .env(.env_sample)
```dotenv
# Configurações do servidor LDAP
LDAP_SERVER = 'ldap://seu_servidor_ldap:389'

# Base do dominio LDAP
LDAP_BASE_DN = 'dc=tlsabara,dc=local'

# Usuário LDAP para acesso e gerenciamento
LDAP_USER_DN = 'cn=ldap_api,dc=G4F,dc=local'

# Senha do usuário LDAP
LDAP_USER_PASSWORD = 'ldap@api@tool'

# Configurações do servidor FastAPI
# Key para is tokens
SECRET_KEY = 'your-secret-key'
# Algoritmo de assinatura
ALGORITHM = 'HS256'
# Tempo de expiração dos tokens em minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token para comunicar com o servidor (Seu custom frontend <> Sevidor do LDAP API)
SERVER_TOKEN = 'devServerToken'

```

### Uso com o docker-compose

#### Sem clonar o projeto (diretament do dockerhub)
```yaml
version: '3.9'

services:
    ldap_api:
        # troque a tag conforme o seu projeto
        image: tlsabara/ldap_api
        ports:
          # porta para o fastapi
          - 8000:8000
        env_file:
          # arquivo .env contendo as variáveis de ambiente
          - .env_sample
# Para usar com AD em localhost basta descomentar
#        extra_hosts:
#            - host.docker.internal:host-gateway
```

#### Com clonagem do projeto
use o `docker-compose build` e `docker-compose up`

## Documentação
A documentação pode ser acessada no endpoint /docs do server.
