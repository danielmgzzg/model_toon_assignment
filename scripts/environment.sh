#!/bin/bash
if [[ -z "${VIRTUAL_ENV}" ]]; then
    if [ ! -d "venv" ]; then
        echo "No virtual environment found. Creating one..."
        python3 -m venv venv
        make install
    fi
    echo "A virtual environment is not currently active."
    source venv/bin/activate
    exec "$@"
else
    echo "A virtual environment is currently active."
fi
