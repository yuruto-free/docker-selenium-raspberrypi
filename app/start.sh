#!/bin/bash

# Waiting for the Grid to be ready
counter=0
ret=1

while [ ${ret} -ne 0 ] && [ ${counter} -lt 60 ]; do
    sleep 1
    counter=$(expr ${counter} + 1)
    curl -sSL ${SELENIUM_URL}/status 2> /dev/null | jq -r '.value.ready' | grep -q "true"
    ret=$?
done
echo "[app]" $(date "+%Y/%m/%d-%H:%M:%S") Selenium ready! "(${counter}sec)"

exec python -u /code/app.py
