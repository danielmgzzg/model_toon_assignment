#!/bin/bash
REGISTRY=$1
REPO_NAME=$2
POD_NAME=${REPO_NAME//_/-}

# Get the latest tag of the image matching the pipeline name
tag=$(kubectl get pod ${POD_NAME}-pod -o jsonpath="{.spec.containers[*].image}" | awk -F":" '{print $NF}')

# Set this image name as an environment variable
export PIPELINE_IMAGE_NAME="${REGISTRY}/${REPO_NAME}:${tag}"

echo $PIPELINE_IMAGE_NAME