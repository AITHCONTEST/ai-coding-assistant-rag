#!/bin/sh
set -e

echo "Running create_database.py..."
python create_database.py

echo "Running inference.py..."
python inference.py