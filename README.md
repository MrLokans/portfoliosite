System requirements
---
- Python 3.6
- pip
- Docker (>=17.10)
- docker-compose (>=1.12)
- tox
- [fabric](http://www.fabfile.org/)
- [osmctools](https://packages.debian.org/search?keywords=osmctools)
- [osm2pgsql](https://wiki.openstreetmap.org/wiki/Osm2pgsql)


Setting environment variables
---
Copy the .env.SAMPLE file to .env file and set all of the required
environment variables for the local environment to work properly.


Running dockerized development environment
-------
The whole application is packed as a set of docker containers, the containers and their relations are
descriped in docker-compose files.

Fill in the required environment variables in the local .env file.

Run the whole stack
```bash
docker-compose up --build
```

Deployment to the production
---
```
fab deploy --set DOCKER_USERNAME=username,DOCKER_PASSWORD=password
```