#!/bin/bash

# Запускаем Xvfb для виртуального дисплея
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &

# Ждем запуска Xvfb
sleep 2

# Запускаем приложение
if [ "$1" = "api" ]; then
    echo "Starting API server..."
    python api_server.py
elif [ "$1" = "cli" ]; then
    echo "Starting CLI application..."
    python main.py
else
    echo "Starting API server by default..."
    python api_server.py
fi
