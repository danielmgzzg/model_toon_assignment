.PHONY: init install environment test clean build-pipeline deploy-pipeline tilt tilt-down
include .env

# Variables
PROJECT_NAME=model_toon_project
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
ENV=dev
PIPELINE_NAME?=model_toon_pipeline
PIPELINE_VERSION?=2.0.5

# Project setup
init:
	./scripts/setup_project.sh $(PROJECT_NAME)

# Install dependencies
install:
	@if [ -f "$(PYTHON)" ]; then \
		$(PYTHON) -m pip install -r requirements/$(ENV).txt; \
	else \
		echo "Virtual environment not found. Please run 'make environment' first."; \
	fi

freeze:
	@if [ -f "$(PYTHON)" ]; then \
		$(PYTHON) -m pip freeze > requirements/$(ENV).txt; \
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

# Tilt up for rapid development
tilt:
	tilt up

# Tilt down to stop development environment
tilt-down:
	tilt down

# Compile Kubeflow pipeline
build-pipeline:
	PIPELINE_NAME=$(PIPELINE_NAME) \
	PIPELINE_TAG=$(PIPELINE_TAG) \
	$(PYTHON) ./pipelines/compile_pipeline.py \
	--output ./pipelines/$(PIPELINE_NAME).yaml

# Deploy pipeline to Kubeflow
deploy-pipeline:
	PIPELINE_NAME=$(PIPELINE_NAME) \
	KUBEFLOW_HOST=$(KUBEFLOW_HOST) \
	$(PYTHON) ./pipelines/deploy_pipeline.py

# To deploy the kubeflow cluster scoped resources including the namespace in Kubernetes manually
kubeflow-namespace:
	kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$(PIPELINE_VERSION)"

# To deploy the kubeflow platform agnostic resources including the deployments and services in Kubernetes manually
kubeflow-pipelines:
	kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$(PIPELINE_VERSION)"

# Fetch remote kubeflow manifests for minikube with kustomize using version
fetch-kubeflow-manifests:
	./scripts/fetch_kubeflow_manifests.sh $(PIPELINE_VERSION)

