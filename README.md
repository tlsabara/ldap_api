# ldap_api

Uma simples api para autenticação LDAP.

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
          - .env_sample
# Para usar com AD em localhost basta descomentar
#        extra_hosts:
#            - host.docker.internal:host-gateway
```

#### Com clonagem do projeto
use o `docker-compose build` e `docker-compose up`

## Documentação
A documentação pode ser acessada no endpoint /docs do server.
