#!/bin/sh

set -e

if [ "$1" = "serve" ]; then
    echo "Starting MCP Server on port 8000..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000
elif [ "$1" = "smoke" ]; then
    echo "Running smoke tests..."
    exec python smoke_test.py
else
    echo "Unknown command: $1"
    echo "Usage: entrypoint.sh [serve|smoke]"
    exit 1
fi
