## Asynchronous RabbitMQ 

### Description
Mini project accomplishing connection between asynchronous API, 
RabbitMQ queue and server with database access. Project contains of:
1) Async API with `GET/POST` methods for sending saving/retrieving task
2) RabbitMQ container which queues task and send them to receivers
3) Receivers get key/data and retrieve it from database or save it

### Stack
Project was pursued with technologies: `aiohttp`, `pika`, `pydantic`, `celery`.

### Installation
Please follow steps:
1) `git clone https://github.com/KonradMarzec1991/async-RabbitMQ.git`
2) `docker-compose up --build` <br />

Docker loads all required dependencies and starts application on port `8000`. <br />
Please ensure that local instance of `RabbitMQ` is not working. If it so, use: <br />
`sudo service rabbitmq-server stop` <br />
to stop local process.

### Testing
With initialization of database `sqlite3` some records are loaded. You can retrieve record `first` without saving it.
Below screenshots shows how to use correctly application (I used here `Postman`).

1) Retrieving data from database
![first](https://user-images.githubusercontent.com/33575891/99188555-ca556280-275c-11eb-929b-606f8060cc8e.png)


2) Saving data to database
![twelve](https://user-images.githubusercontent.com/33575891/99188602-04266900-275d-11eb-9315-44ffddc30546.png)

3) Retrieving already saved data
![twelve_retrieve](https://user-images.githubusercontent.com/33575891/99188607-08528680-275d-11eb-9a78-104a219408b2.png)

4) Retrieving from database record that does not exist
![wrong](https://user-images.githubusercontent.com/33575891/99188608-0be60d80-275d-11eb-98e5-041b90344acc.png)
