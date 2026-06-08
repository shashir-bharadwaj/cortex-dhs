# FROM python:3.11-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /usr/src/app

# # Install system dependencies
# RUN apt-get update && apt-get install -y build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY ./app ./app

# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



FROM python:3.12-slim

WORKDIR /app

# Install netcat so docker-compose can wait for Postgres
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000