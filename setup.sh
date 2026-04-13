#!/bin/bash
set -e

echo "==> Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "==> Installing requirements..."
pip install -r requirements.txt

echo "==> Running migrations..."
python manage.py migrate

echo "==> Creating demo content..."
python manage.py setup_demo
