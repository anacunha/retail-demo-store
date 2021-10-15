# Retail Demo Store location Service

The location web service provides an API for retrieving locations to support to Location Services demo in Find My Brew.

## Local Development

The location service can be built and run locally (in Docker) using Docker Compose. See the [local development instructions](../) for details. **From the `../src` directory**, run the following command to build and deploy the service locally.

```console
foo@bar:~$ docker-compose up --build location
```

Once the container is up and running, you can access it in your browser or with a utility such as [Postman](https://www.postman.com/) at [http://localhost:8009](http://localhost:8009).
