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

RUN chmod +x /code/init-db.sh
RUN chmod +x /code/docker-entrypoint.sh
RUN chmod +x /code/wait-for-it.sh

ENTRYPOINT ["/code/docker-entrypoint.sh"]