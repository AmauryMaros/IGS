# Docker commands

1. Build the Docker image:

```bash
docker build -t my-container .
```
```bash
# Platform specific - amymr = username
docker buildx build --platform linux/amd64,linux/arm64 -t amymr/my-container --push .
```

2. Run the Docker container interactively:

```bash
docker run -it my-container bash
```

```bash
# Platform specific
docker run --platform linux/amd64 -it amymr/my-container bash
docker run --platform linux/amd64 -it amymr/my-container sh
```

3. Run the Docker container with a mouted volume:
```bash
docker run -d -p 8501:8501 \
    --name my-container \
    -v Path/to/Mount_data/Data:/app/app/Data \ #Volume1
    -v Path/to/Mount_data/Medias:/app/app/Medias \ #Volume2
    my-container
```

4. Usefull
```bash
# List images and container
docker images
docker ps
docker ps -a

# Stop and remove 1 container
docker stop <containerID>
docker remove >containerID>

# Remove image
docker rmi <imageID>

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)
```
