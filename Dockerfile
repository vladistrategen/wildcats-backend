# Use the official slim Python image as a base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
        pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port the app runs in
EXPOSE 8000

# Specify the command to run on container start
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "localhost:8000"]
