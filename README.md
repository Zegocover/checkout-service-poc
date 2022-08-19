### Docker build

To run first build the docker image using 

```
docker-compose build
```

Then once the images have been built run
```
docker-compose up
```

By default this will run on http://localhost:8000/


### DB Setup

Once the docker container is running you can setup the db

The following commands will set up aerich to run against the tortoise db config found in db.py
```
docker-compose exec web aerich init -t db.TORTOISE_ORM
docker-compose exec web aerich init-db
```

To then create any new migrations use the following command
```
docker-compose exec web aerich migrate
```

To run those migrations into the db use the following command
```
docker-compose exec web aerich upgrade
```

### DB Connect

Once the db is setup and running you can then connect by opening up psql via docker
```
docker-compose exec web-db psql -U postgres
```
When psql is running connect to the db with
```
\c web
```

To connect using a database app of your choice use the username and password found in docker-compose.yml and use the following url:
```
jdbc:postgresql://localhost:19027/web
```
