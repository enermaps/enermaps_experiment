Base skeleton for experimenting around what enermap could become

# Codestyle

Just use ![black](https://github.com/psf/black) for all python code.

Pylint is also nice to have and is recommended but not enforced.

# Local Dev environment

Install docker and docker-compose

then run

	docker-compose up

this will start a local geoserver and a local postgres data. 
The local geoserver will be available at http://127.0.0.1:5432 and the geoserver at http://127.0.0.1:8080
