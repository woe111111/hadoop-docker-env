#!/bin/sh

set -e

sed -i "s#HIVE_SERVER_HOST#${HIVE_SERVER_HOST}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#HIVE_SERVER_PORT#${HIVE_SERVER_PORT}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#HIVE_METASTORE_HOST#${HIVE_METASTORE_HOST}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#HIVE_METASTORE_PORT#${HIVE_METASTORE_PORT}#g" /usr/share/hue/desktop/conf/hue.ini

sed -i "s#ENGINE#${ENGINE}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#HOST#${HOST}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#PORT#${PORT}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#USER#${USER}#g" /usr/share/hue/desktop/conf/hue.ini
sed -i "s#PASSWORD#${PASSWORD}#g" /usr/share/hue/desktop/conf/hue.ini



exec "$@"