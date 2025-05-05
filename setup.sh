#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install flask pandas

echo "Creating upload folder..."
mkdir -p uploads

echo "Initializing SQLite database..."
sqlite3 bacteria.db < schema.sql

echo "Setup complete. Run the app with: source venv/bin/activate && python app.py"
