## Run all components at once.

You need the [aquas_front](https://github.com/jaconsta/aquas_front) image built first.

Run

```
docker-compose -f config/compose/compose-dev.yml up
```

- Access the Front end service from [http://localhost:8080]()
- Access the Api server from [http://localhost:8000]()

## Installation

Install dependencies

`pip install -r requirements.txt`

Install an MQTT service like [Mosquitto](https://mosquitto.org/)


## Run commands

**Run server** `python manage.py runserver 0.0.0.0:8000`

### Docker configuration

Build image
```
docker build . -t aquas_web
```

Run the container
```
docker run -d -p 8000:8000 --name=aquas_web_dev aquas_web
```

Start / Stop container
```
docker container <start/stop> <container_id/name>
```
