# Use a base Python image
FROM python:3.9-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and update all packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        libffi-dev \
        libssl-dev \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Upgrade pip and setuptools to the latest versions to mitigate vulnerabilities
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install project dependencies, ensuring they're updated
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project including the modules directory
COPY . .

# Command to run your application
CMD ["python", "main.py"]

