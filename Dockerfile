# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Install any needed packages specified in requirements.txt
COPY requirements/dev.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set a default command or entrypoint (e.g., python or a specific script)
ENTRYPOINT ["python"]