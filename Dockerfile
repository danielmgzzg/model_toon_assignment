# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Get build arguments
ARG git_repo_url
ARG azure_client_id
ARG azure_tenant_id
ARG azure_client_secret
ARG azure_storage_container_name
ARG azure_storage_account_name

# Set environment variables
ENV GIT_REPO_URL $git_repo_url
ENV AZURE_CLIENT_ID $azure_client_id
ENV AZURE_TENANT_ID $azure_tenant_id
ENV AZURE_CLIENT_SECRET $azure_client_secret
ENV AZURE_STORAGE_CONTAINER_NAME $azure_storage_container_name
ENV AZURE_STORAGE_ACCOUNT_NAME $azure_storage_account_name

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && \
    apt-get install -y curl lsb-release gnupg && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone $GIT_REPO_URL .
RUN git status

# Copy the current directory contents into the container at /app
RUN rm -R /app/src
COPY ./src /app

# Install any needed packages specified in requirements.txt
COPY requirements/dev.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN  dvc remote add -d -f az-blob azure://$AZURE_STORAGE_CONTAINER_NAME 
RUN  dvc remote modify --local az-blob account_name $AZURE_STORAGE_ACCOUNT_NAME
RUN  dvc remote modify --local az-blob tenant_id $AZURE_TENANT_ID
RUN  dvc remote modify --local az-blob client_id $AZURE_CLIENT_ID
RUN  dvc remote modify --local az-blob client_secret $AZURE_CLIENT_SECRET
RUN  dvc pull

# Set a default command or entrypoint (e.g., python or a specific script)
ENTRYPOINT ["python"]