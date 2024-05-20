docker compose down
docker volume ls
# docker volume rn openldap_camara_ldap_confi
docker volume rm openldap_camara_ldap_config1
docker volume rm openldap_camara_ldap_data1
# docker compose up -d --force-recreate
docker compose ps