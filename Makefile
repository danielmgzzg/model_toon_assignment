.PHONY: init install environment test clean

# Variables
PROJECT_NAME=model_toon_project
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

# Project setup
init:
	./scripts/setup_project.sh $(PROJECT_NAME)

# Install dependencies
install:
	@if [ -f "$(PYTHON)" ]; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "Virtual environment not found. Please run 'make environment' first."; \
	fi

# Create the virtual environment
environment:
	./scripts/environment.sh

# Activate the virtual environment
activate:
	@echo "To activate the virtual environment, run 'source $(VENV_NAME)/bin/activate'"

# Run tests
test:
	$(PYTHON) -m unittest discover -s $(PROJECT_NAME)/tests -p 'test*.py'

# Clean up pycache and temporary files
clean:
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete