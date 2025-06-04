# services/genai-inference-service/Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies needed for some Python packages (e.g., numpy)
# In a production environment, you might need more specific ones depending on the base image
# and actual libraries used. This is a common set.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5003

CMD ["python", "app.py"]