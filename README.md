# FastApi application with Celery Broker
### The application includes a loigku to get ip address from external api and save it to database. 

## Technologies used 
- **FastApi**
- **Celery**
- **Peewe ORM**
- **RabbitMQ**
- **Swagger Docs**
- **MySQL**
- **UnitTests**
- **Uvicorn (On Server live preview)**** 
- **Nginx (On Server live preview)**

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
