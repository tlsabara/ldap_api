# Configuração Local do OpenLDAP

Este repositório contém a configuração necessária para implantar um serviço OpenLDAP localmente usando Docker Compose, incluindo a configuração inicial de um grupo e dois usuários.

## Estrutura de Diretórios

```
ldap-setup/
|-- docker-compose.yml
|-- bootstrap/
|-- bootstrap.sh
|-- users.ldif
```


## Instruções de Uso

### Lembrete Importante
Senha do Administrador: Se você alterar a senha do administrador no arquivo docker-compose.yml, certifique-se de atualizar também a senha no script bootstrap/bootstrap.sh. Isso é necessário para garantir que o script possa autenticar corretamente e realizar as configurações iniciais.


### 1. Preparação
Clone o repositório e navegue até o diretório `ldap-setup`. Garanta que todos os scripts em `bootstrap/` estão com permissão de execução. Você pode definir isso com o comando:

```bash
chmod +x bootstrap/*.sh
```

### 2. Configuração
Antes de iniciar o serviço, revise o arquivo docker-compose.yml e o bootstrap/bootstrap.sh para garantir que as configurações, especialmente as senhas, estão corretas e de acordo com as suas necessidades.

### 3. Inicialização
Para iniciar o servidor LDAP, execute o seguinte comando no diretório ldap-setup:

```
docker-compose up
```

Este comando irá levantar o serviço OpenLDAP e aplicar automaticamente as configurações de usuários e grupos definidas no arquivo users.ldif.

### 4. Acesso
Após a inicialização, o serviço LDAP estará acessível via localhost nas portas 389 (padrão) e 636 (SSL). Utilize um cliente LDAP de sua escolha para conectar-se ao servidor usando as credenciais de administrador.


