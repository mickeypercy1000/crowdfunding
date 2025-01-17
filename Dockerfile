# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set environment variables to ensure non-interactive installation and default encoding
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
