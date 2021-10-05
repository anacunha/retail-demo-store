# Retail Demo Store locations Service

The locations web service provides an API for retrieving all brewery/bar locations in Find My Brew.

This service has two endpoints

## Local Development

The location service can be built and run locally (in Docker) using Docker Compose. See the [local development instructions](../) for details. **From the `../src` directory**, run the following command to build and deploy the service locally.

```console
foo@bar:~$ docker-compose up --build locations
```

Once the container is up and running, you can access it in your browser or with a utility such as [Postman](https://www.postman.com/) at [http://localhost:8010](http://localhost:8010).
