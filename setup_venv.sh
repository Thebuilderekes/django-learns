#!/bin/bash
# Script to set up virtual environment for Django project

echo "Setting up virtual environment for bookr project..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo ""
echo "✅ Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "    source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "    deactivate"
echo ""
echo "To run the Django server:"
echo "    python manage.py runserver"
