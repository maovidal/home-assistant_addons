#!/usr/bin/with-contenv bashio

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output
# is sent straight to the container log.
# This also ensures that no partial output is held in a buffer somewhere and
# never written in case the python application crashes.
export PYTHONUNBUFFERED=1

bashio::log.info "Creating configuration file from options..."

CONFIG_PATH=/config.py

{
    echo "DEBUG_MODE = \"$(bashio::config 'debug')\"";
    echo "CUSTOM_PORT = $(bashio::addon.port '514/udp')";
    echo "ENDPOINT_1 = \"$(bashio::config 'endpoint_1')\"";
    echo "ENDPOINT_2 = \"$(bashio::config 'endpoint_2')\"";
    echo "TO_SEEK_1 = \"$(bashio::config 'to_seek_1')\"";
    echo "TO_SEEK_2 = \"$(bashio::config 'to_seek_2')\"";
    echo "PAYLOAD_1 = '$(bashio::config 'payload_1')'";
    echo "PAYLOAD_2 = '$(bashio::config 'payload_2')'";

} > "${CONFIG_PATH}"

bashio::log.info "Asking Python to run SL2HA..."

python3 /sl2ha.py
