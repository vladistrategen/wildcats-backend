# Wildcats Backend

## Overview

Welcome to the Wildcats Backend project! This repository serves as the backend component of our application. Below, you'll find instructions on setting up the project and getting started with development.

## Prerequisites

Before you can run this project and begin development, you need to ensure you have Docker installed. To check if Docker is installed, open your terminal and run the following command:

```bash
$ docker -v
```

If Docker is installed, you should see output similar to the following:

```
Docker version 24.0.6, build ed223bc
```

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine:

```bash
$ git clone https://github.com/vladistrategen/wildcats-backend.git
```

2. Set up the environment variables:

   - Create a `.env` file in the project's root directory.

   - You can use the included `.env.example` file as a starting point. Update the values in the `.env` file to match your specific configuration.

3. Run the Project:

   - With Docker installed and the environment variables configured, everything should be automatically set up and configured.

   - Now create the external volume for static file sharing with the react frontend contianer:
   ```bash
   $ docker volume create static_files
   ```

   - To start the project, navigate to the project's Docker directory by running:
   ```bash
   $ cd Docker
   ```
   and then execute the following commands:

     ```bash
     $ docker compose build

     $ docker compose up
     ```

     - To run the container terminal inside VSCode for live development, open a new Powershell terminal and run:

     ```powershell
     C:\> docker exec -it wildcats-web-1 /bin/sh
     ```

4. Access the Application:

   - Once the project is running, you can access it in your web browser by visiting [http://localhost:8000](http://localhost:8000).
