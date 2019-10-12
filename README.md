Project description
---
This project is an umbrella project for various pet projects of mine for past several years.
The first one is a website of mine built around django and wagtail that describes my work experience,
projects, possible talks and blog entries (hope there will be any in near future :)).

Second one - is the [parser](https://github.com/MrLokans/onliner-agent-finder) of local Belarus web-site dedicating to providing info about apartment rental / selling.

It is a web crawler written in Python scrappy, small ETL integrated with django ORM for data persistence and a Telegram reporter of results.

For more info on high-level architecture please refer to docs section of the repository, there is a high-level Draw.io diagram representing the 5.000 feet overview of the project.

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

Commands
---
Running parser and filling in initial database
```
python manage.py scrapeapartments
```

Deployment to the production
---
Deploy built image uploaded to the registry
```
fab deploy --set DOCKER_USERNAME=username,DOCKER_PASSWORD=password
```

Renew HTTPS certificates
```
fab renew_certificates
```
