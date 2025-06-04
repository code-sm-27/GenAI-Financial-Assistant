# services/api-gateway/Dockerfile
#
# Dockerfile for the API Gateway service.
# Builds a Docker image containing the Flask application, its dependencies,
# and the HTML templates/static files.

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
# This includes app.py, config.py, and the 'templates' and 'static' directories.
COPY . .

# Expose the port that the API Gateway will run on.
# This informs Docker that the container listens on the specified network port.
EXPOSE 5000

# Define environment variables for Flask.
# FLASK_APP: Specifies the main Flask application file.
# FLASK_ENV: Sets the environment (development/production).
#            Set to 'production' for a more robust deployment.
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the application.
# `flask run` is suitable for development. For production, consider Gunicorn.
# --host 0.0.0.0: Makes the Flask app accessible from outside the container.
# --port 5000: Specifies the port the Flask app listens on.
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]