.PHONY: init install environment test clean build-pipeline deploy-pipeline tilt tilt-down data
include .env

# Variables
PROJECT_NAME=model_toon
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
ENV=dev
PIPELINE_NAME?=model_toon_pipeline
PIPELINE_VERSION?=2.0.5


# Install dependencies
install:
	@if [ -f "$(PYTHON)" ]; then \
		$(PYTHON) -m pip install -r requirements/$(ENV).txt; \
	else \
		echo "Virtual environment not found. Please run 'make environment' first."; \
	fi

data:
	$(PYTHON) -m dvc remote add -d az-blob azure://${AZURE_STORAGE_CONTAINER_NAME}
	$(PYTHON) -m dvc remote modify --local az-blob account_name ${AZURE_STORAGE_ACCOUNT_NAME}
	$(PYTHON) -m dvc remote modify --local az-blob tenant_id ${AZURE_TENANT_ID}
	$(PYTHON) -m dvc remote modify --local az-blob client_id ${AZURE_CLIENT_ID}
	$(PYTHON) -m dvc remote modify --local az-blob client_secret ${AZURE_CLIENT_SECRET}
	$(PYTHON) -m dvc pull

freeze:
	@if [ -f "$(PYTHON)" ]; then \
		$(PYTHON) -m pip freeze > requirements/$(ENV).txt; \
	else \
		echo "Virtual environment not found. Please run 'make environment' first."; \
	fi

# Create the virtual environment
environment: data
	./scripts/environment.sh

# Activate the virtual environment
activate:
	@echo "To activate the virtual environment, run 'source $(VENV_NAME)/bin/activate'"

# Run tests
test:
	export PYTHONPATH=$$PYTHONPATH:"src" && \
	echo $$PYTHONPATH && \
	$(PYTHON) -m unittest discover -s tests -p 'test*.py'

# Clean up pycache and temporary files
clean:
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

minikube-init:
	@ctlptl get cluster minikube && ctlptl delete cluster minikube || true
	@ctlptl create cluster minikube --registry=ctlptl-registry --kubernetes-version=v1.23.3

minikube-start:
	minikube start

build:
	docker  build  . --tag $(PROJECT_NAME):latest  \
	--build-arg git_repo_url=$(GIT_REPO_URL)  \
	--build-arg azure_client_id=$(AZURE_CLIENT_ID) \
	--build-arg azure_client_secret=$(AZURE_CLIENT_SECRET) \
	--build-arg azure_tenant_id=$(AZURE_TENANT_ID) \
	--build-arg azure_storage_container_name=$(AZURE_STORAGE_CONTAINER_NAME) \
	--build-arg azure_storage_account_name=$(AZURE_STORAGE_ACCOUNT_NAME)

# Tilt up for rapid development
tilt:
	PIPELINE_NAME=$(PIPELINE_NAME) \
	GIT_REPO_URL=$(GIT_REPO_URL) \
	AZURE_CLIENT_ID=$(AZURE_CLIENT_ID) \
	AZURE_STORAGE_CONTAINER_NAME=${AZURE_STORAGE_CONTAINER_NAME} \
	AZURE_STORAGE_ACCOUNT_NAME=${AZURE_STORAGE_ACCOUNT_NAME} \
	AZURE_CLIENT_SECRET=$(AZURE_CLIENT_SECRET) \
	AZURE_TENANT_ID=$(AZURE_TENANT_ID) \
	tilt up

# Tilt down to stop development environment
tilt-down:
	tilt down

# Compile Kubeflow pipeline (Used by Tilt)
build-pipeline:
	PIPELINE_IMAGE_NAME=$(shell ./scripts/get_image_tag.sh $(REGISTRY) $(PIPELINE_NAME) | tail -n 1) \
	PIPELINE_NAME=$(PIPELINE_NAME) \
	PIPELINE_TAG=$(PIPELINE_TAG) \
	$(PYTHON) ./pipelines/compile_pipeline.py \
	--output ./pipelines/$(PIPELINE_NAME).yaml

# Deploy pipeline to Kubeflow (Used by Tilt)
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

azure-svc-acc:
	az ad sp create-for-rbac --name "$(PROJECT_NAME)_service_account"

azure-role-subscription:
	az role assignment create --assignee $(AZURE_CLIENT_ID) --role Contributor --scope /subscriptions/$(AZURE_SUBSCRIPTION_ID)/resourceGroups/$(RESOURCE_GROUP)

azure-role-storage:
	az role assignment create --assignee $(AZURE_CLIENT_ID) --role "Storage Blob Data Contributor" --scope /subscriptions/$(AZURE_SUBSCRIPTION_ID)/resourceGroups/$(AZURE_RESOURCE_GROUP)/providers/Microsoft.Storage/storageAccounts/$(AZURE_STORAGE_ACCOUNT_NAME)/blobServices/default/containers/$(AZURE_STORAGE_CONTAINER_NAME)

clean-pods:
	kubectl delete pods --field-selector=status.phase=Succeeded --namespace kubeflow