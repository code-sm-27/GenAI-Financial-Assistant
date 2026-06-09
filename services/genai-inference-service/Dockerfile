# Stage 1: Build
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim as development
WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*
COPY . /app/
EXPOSE 5002
CMD ["python", "app.py"]

# Stage 3: Production
FROM development as production
CMD ["python", "app.py"]