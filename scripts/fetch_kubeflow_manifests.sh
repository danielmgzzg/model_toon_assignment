#!/bin/bash
# Fetch Kubeflow manifests and save them locally

PIPELINE_VERSION="$1"
mkdir -p deployments/kubeflow

# Fetch Kubeflow namespace resources
kubectl kustomize "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION" > deployments/kubeflow/namespace.yaml

# Fetch Kubeflow pipeline resources
kubectl kustomize "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION" > deployments/kubeflow/pipelines.yaml
