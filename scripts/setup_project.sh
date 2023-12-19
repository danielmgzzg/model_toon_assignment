#!/bin/bash

# Check if a project name is provided
if [ -z "$1" ]; then
  echo "No project name provided. Usage: setup_project.sh <project_name>"
  exit 1
fi

# Use the provided project name
PROJECT_NAME="$1"

# Create the src directory and Python files
mkdir -p src
touch src/__init__.py
touch src/data_preparation.py
touch src/model.py
touch src/training.py
touch src/evaluation.py
touch src/inference.py

# Create the notebooks directory and the example Jupyter notebook
mkdir -p notebooks
echo "# Example Usage" > notebooks/example_usage.ipynb

# Create the tests directory and Python test file
mkdir -p tests
touch tests/__init__.py
touch tests/test_model.py

# Create the requirements.txt, setup.py, .gitignore, and README.md files
touch requirements.txt
echo -e "from setuptools import setup, find_packages\n\nsetup(name='$PROJECT_NAME', version='1.0', packages=find_packages())" > setup.py
echo -e "# '$PROJECT_NAME'\n\nThis project contains ..." > README.md
echo -e "venv/\n__pycache__/\n*.pyc" > .gitignore

echo -e "Project structure has been set up.\nPlease add requirements to requirements.txt and run 'pip install -r requirements.txt' to install them."

