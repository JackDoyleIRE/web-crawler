# Dockerfile.test

# Use the same base image as your main application
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install required packages (if you have a requirements.txt)
RUN pip install -r requirements.txt

# Command to run tests
CMD ["python3", "test_crawler.py"]
