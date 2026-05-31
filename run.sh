#!/usr/bin/with-contenv bashio

MQTT_HOST=$(bashio::config 'mqtt_host')
MQTT_PORT=$(bashio::config 'mqtt_port')
MQTT_USER=$(bashio::config 'mqtt_user')
MQTT_PASSWORD=$(bashio::config 'mqtt_password')
POLL_INTERVAL=$(bashio::config 'poll_interval')

export MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD POLL_INTERVAL

bashio::log.info "Starting APC UPS MQTT..."
bashio::log.info "MQTT Broker: ${MQTT_HOST}:${MQTT_PORT}"
bashio::log.info "Poll interval: ${POLL_INTERVAL}s"

exec python3 /app/apc_mqtt.py
