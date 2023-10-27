# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

# Copy project
COPY src/ /app/
COPY .env /app/

# Copy scripts and grant execution permissions
COPY Scripts/docker-entrypoint.sh /app/
COPY Scripts/init-db.sh /app/
COPY Scripts/wait-for-it.sh /app/
RUN chmod +x /app/docker-entrypoint.sh /app/init-db.sh /app/wait-for-it.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
