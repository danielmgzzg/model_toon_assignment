# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Get build arguments
ARG git_repo_url
ARG git_token
ARG azure_client_id
ARG azure_tenant_id
ARG azure_client_secret

# Set environment variables
ENV GIT_REPO_URL $git_repo_url
ENV GIT_TOKEN $git_token
ENV AZURE_CLIENT_ID $azure_client_id
ENV AZURE_TENANT_ID $azure_tenant_id
ENV AZURE_CLIENT_SECRET $azure_client_secret

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && \
    apt-get install -y curl lsb-release gnupg && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://$GIT_TOKEN@$GIT_REPO_URL .
RUN git status

# Copy the current directory contents into the container at /app
RUN rm -R /app/src
COPY ./src /app

# Install any needed packages specified in requirements.txt
COPY requirements/dev.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Log in to Azure with the service account credentials for DVC with Blob Storage
RUN az login --service-principal \
    --username $AZURE_CLIENT_ID \
    --password $AZURE_CLIENT_SECRET \
    --tenant $AZURE_TENANT_ID

# copy DVC configuration 
COPY .dvc/config /app/.dvc/config

# Pull data from DVC
RUN dvc pull

# Set a default command or entrypoint (e.g., python or a specific script)
ENTRYPOINT ["python"]