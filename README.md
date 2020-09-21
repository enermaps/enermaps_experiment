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

Install docker and docker-compose

then run

	docker-compose up

this will start a local geoserver and a local postgres data. 
The local postgresql will be available at http://127.0.0.1:5432 and the geoserver at http://127.0.0.1:8000

You can setup the geoserver if you started it for the first time by running:

	#this will export configuration variable into the current shell
	export $(cat .env | xargs) 
	./importer/geoserver_init.py

Note that you will need to have the requests library installed first.
