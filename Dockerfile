# Dockerfile

# Use Python 3.9 as base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

RUN pip install -r requirements.txt

# Expose port 8000 for the local web server (if needed for testing or crawling)
EXPOSE 8000

# Run the main.py file to start the CLI app
CMD ["python3", "main.py", "--start"]

