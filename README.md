# AMIO_CUSTOM_API
Custom API to work on AMIO project

This repository provides a tiny FastAPI service that serves a static JSON payload at the route `/AMIO-API`.

How to build and run with Docker

```bash
# build the image (run from repo root)
docker build -t amio-custom-api .

# run mapping container port 80 to host port 8080
docker run -p 8080:80 --rm amio-custom-api
```

After starting, the endpoint will be available at http://<HOST_IP>:8080/AMIO-API

Notes about running on your OVH Ubuntu server

- On the server you can run the same docker run command. To expose it on the root path `http://IP/AMIO-API`, map the container port to a host port that your web server or reverse proxy (nginx) will forward to. A simple approach is to run the container on port 80 (requires root) or use a reverse proxy.

Example using Docker (host port 80):

```bash
sudo docker run -p 80:80 --restart unless-stopped -d amio-custom-api
```

Or configure nginx to reverse-proxy `IP/AMIO-API` to `http://127.0.0.1:8080/AMIO-API` if you prefer not to run the container as root.

Docker Compose + nginx example

The included `docker-compose.yaml` runs the FastAPI container and an `nginx` container that reverse-proxies `/AMIO-API` to the app. The app runs inside the container as a non-root user and listens on port `8000` internally.

Start with:

```bash
docker-compose up -d --build
```

Access the endpoint at:

```
http://<HOST_IP>/AMIO-API
```

If you need to use a reverse proxy on the server instead of the provided nginx container, place `deploy/nginx.conf` in your nginx configuration (or adapt it) and point `/AMIO-API` to `http://127.0.0.1:8000/AMIO-API`.

