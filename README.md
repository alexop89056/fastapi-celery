# FastApi application with Celery Broker

## Overview
The application includes a logic to get ip address from external api and save it to database. 

## Technologies used 
- **FastApi**
- **Celery**
- **RestApi**
- **Jwt Authorization**
- **Peewe ORM**
- **RabbitMQ**
- **Swagger Docs**
- **MySQL**
- **UnitTests**
- **Uvicorn (On Server live preview)**
- **Nginx (On Server live preview)**

## Installation

To install the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/alexop89056/fastapi-celery.git
2. Navigate to the project directory:
 
    ```bash
    cd fastapi-celery
3. Install dependencies:
 
    ```bash
    pip install -r app/requirements.txt

## Usage
- Start Project with a uvicorn server:

   ```bash
   uvicorn app:app

## Project Architecture
- **app**: Root folder
  - **auth**: Jwt tokens logic
  - **dependencies**: Main dependencies of api routes
  - **models**: Database and Pydantic models
  - **routes**: Api Routes
  - **tasks**: Celery tasks
  - **celery_app.py**: Celery entrypoint
  - **config.py**: Main config of app
  - **local_config.py**: Local config (Something like .env file)
  - **requirements.txt**: Modules list
- **unit_test.py**: Py file to run unit tests

## License
This project is licensed under the MIT License - see the [main page](https://mit-license.org/) for the details.
