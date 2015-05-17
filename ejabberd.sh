#!/bin/bash
docker run -d -p "4560:4560" -p "5280:5280" \
    -e "EJABBERD_REGISTER_TRUSTED_NETWORK_ONLY=true" \
    -e "EJABBERD_ADMIN=${PYEJABBERD_TESTS_USERNAME:=admin}@${PYEJABBERD_TESTS_XMPP_DOMAIN:=example.com}" \
    -e "EJABBERD_ADMIN_PWD=${PYEJABBERD_TESTS_PASSWORD:=admin}" \
    -e "XMPP_DOMAIN=${PYEJABBERD_TESTS_XMPP_DOMAIN:=example.com}" \
    -e "EJABBERD_MUC_CREATE_ADMIN_ONLY=true" \
    -e "EJABBERD_REGISTER_ADMIN_ONLY=true" \
    -e "EJABBERD_MOD_ADMIN_EXTRA=true" \
    -e "EJABBERD_MOD_MUC_ADMIN=true" \
    -e "EJABBERD_WEB_ADMIN_SSL=false" \
    -e "EJABBERD_S2S_SSL=true" \
    dirkmoors/ejabberd
