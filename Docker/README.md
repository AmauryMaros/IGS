# Docker commands

1. Build the Docker image:

```bash
docker build -t my-container .
```

2. Run the Docker container interactively:

```bash
docker run -it my-container bash
```

3. Run the Docker container with a mouted volume:
```bash
docker run -d -p 8501:8501 \
    --name my-container \
    -v Path/to/Mount_data/Data:/app/app/Data \
    -v Path/to/Mount_data/Medias:/app/app/Medias \
    mgcst_app_mount
```
