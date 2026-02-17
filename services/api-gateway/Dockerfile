FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use python directly to ensure our custom DB init logic runs
CMD ["python", "app.py"]