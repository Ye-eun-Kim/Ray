# Dockerfile

FROM python:3.11-slim

WORKDIR /app


# Copy project files
COPY Ray/ /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# MongoDB configuration in scrapy settings
# Add to oliveyoung/settings.py
MONGO_URI = 'mongodb://mongodb-service:27017'
MONGO_DATABASE = 'olive_db'