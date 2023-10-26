# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client
# Copy project
COPY . /code/

RUN chmod +x init-db.sh
RUN chmod +x docker-entrypoint.sh
RUN chmod +x wait-for-it.sh

COPY wait-for-it.sh /code/
COPY docker-entrypoint.sh /code/
COPY init-db.sh /code/

ENTRYPOINT ["/code/docker-entrypoint.sh"]