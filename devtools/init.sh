#!/bin/bash

/opt/bitnami/scripts/openldap/entrypoint.sh /opt/bitnami/scripts/openldap/run.sh &

sleep 20

ldapmodify -Y EXTERNAL -H ldapi:/// -f /container/service/slapd/assets/config/bootstrap/ldif/custom/creation.ldif

ldapadd -x -D "cn=ldap_api,dc=tlsabara,dc=local" -w ldap@api@tool -f /container/service/slapd/assets/config/bootstrap/ldif/custom/users.ldif

# ldapmodify -Y EXTERNAL -H ldapi:/// -f /container/service/slapd/assets/config/bootstrap/ldif/custom/addPermission.ldif

wait $!
