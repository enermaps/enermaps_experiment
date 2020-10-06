Base skeleton for experimenting around what enermap could become
# Importer 

Import a local file into the geoserver.

# geoserver

Docker image of the enermap geoserver.

# postgis

Postgres database with postgis based on the camptocamp image.

## Codestyle

Just use ![black](https://github.com/psf/black) for all python code.

Pylint is also nice to have and is recommended but not enforced.

The import order and location be fixed to match the pep8 using ![isort](https://github.com/PyCQA/isort)

# Local Dev environment

First, clone this repository, then git@github.com:enermaps/Hotmaps-toolbox-service.git in the same directory.
You should end up with the following directory organisation:

* root
    * Hotmaps-toolbox-service
    * enermaps

Install docker and docker-compose

then run

	docker-compose up

this will start the following set of services:

The local postgresql will be available at 127.0.0.1:5432 
the geoserver at http://127.0.0.1:8000/geoserver
the api server at http://127.0.0.1:9000/api
the frontend at http://127.0.0.1:7000/api
the whole application can be accessed trough http://127.0.0.1:2000

You can setup the geoserver if you started it for the first time by running:

	#this will export configuration variable into the current shell
	export $(cat .env | xargs) 
	./importer/geoserver_init.py

Note that you will need to have the requests library installed first.

If you are only interested in a subset of services, you can check for those service in the docker-compose.yaml file and only start the one you are interested in. For example for only starting the postgis database and the geoserver:

	docker-compose up geoserver db
