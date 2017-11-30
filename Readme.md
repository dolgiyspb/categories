## Requirmenets

```
$ docker --version
Docker version 17.11.0-ce, build 1caf76c
$ docker-compose --version
docker-compose version 1.17.0, build ac53b73

```

## Build

```
$ docker-compose build
```

## Run

```
$ docker-compose up
...
...

web_1  | System check identified no issues (0 silenced).
web_1  | November 30, 2017 - 12:22:56
web_1  | Django version 1.11.7, using settings 'am_project.settings'
web_1  | Starting development server at http://0.0.0.0:8000/
web_1  | Quit the server with CONTROL-C.

```

In another terminal:
```
$ curl -X POST -H "Content-type:application/json" 127.0.0.1:8000/categories/ -d '{"name":"Category 1", "children":[{"name":"Category 1.2"}]}'
{"id":1,"name":"Category 1","children":[{"id":2,"name":"Category 1.2","children":[]}]}
$ curl -H "Content-type:application/json" 127.0.0.1:8000/categories/1/
{"id":1,"name":"Category 1","children":[{"id":2,"name":"Category 1.2"}],"parents":[],"siblings":[]}
```

## Testing
### Check db container running
```
$ docker-compose ps
      Name                    Command               State           Ports
----------------------------------------------------------------------------------
categories_db_1    docker-entrypoint.sh mysqld      Up      3306/tcp

```
### Run test

```
$ docker-compose run --rm web python manage.py test -v 3
```