## Installation

Pull the image

**Note** There are no more submodules now.
 
Install git submodules
```
git submodule update --init --recursive
```

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
