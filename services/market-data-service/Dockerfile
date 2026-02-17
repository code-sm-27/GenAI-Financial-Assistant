# services/market-data-service/Dockerfile
#
# Dockerfile for the Market Data Service.
# Builds a Docker image containing the Flask application and its dependencies.

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install the Python dependencies
# --no-cache-dir: Prevents pip from storing cache, reducing image size.
# -r requirements.txt: Installs all packages listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the working directory.
# This includes app.py and data_fetcher.py.
COPY . .

# Expose the port that the Market Data Service will run on.
EXPOSE 5001

# Define environment variables for Flask.
# FLASK_APP: Specifies the main Flask application file.
# FLASK_ENV: Sets the environment (development/production).
#            Set to 'production' for a more robust deployment.
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the application.
# `flask run` is suitable for development. For production, consider Gunicorn.
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]