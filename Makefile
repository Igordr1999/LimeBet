.PHONY: docs clean

COMMAND = sudo docker-compose run --rm djangoapp /bin/bash -c

all: build test

restart: stop runfull

production: stop makemigrations migrate collectstatic runprod

build:
	sudo docker-compose build

stop:
	sudo docker-compose stop

run:
	sudo docker-compose up

runprod:
	sudo docker-compose up -d

makemigrations:
	sudo docker-compose run --rm djangoapp limebet/manage.py makemigrations

migrate:
	$(COMMAND) 'cd limebet; for db in default database2; do ./manage.py migrate --database=$${db}; done'

collectstatic:
	sudo docker-compose run --rm djangoapp limebet/manage.py collectstatic --no-input

makemessages:
	sudo docker-compose run --rm djangoapp limebet/manage.py makemessages -a

compilemessages:
	sudo docker-compose run --rm djangoapp limebet/manage.py compilemessages

check: checksafety checkstyle

test:
	$(COMMAND) "pip install tox && tox -e test"

checksafety:
	$(COMMAND) "pip install tox && tox -e checksafety"

checkstyle:
	$(COMMAND) "pip install tox && tox -e checkstyle"

coverage:
	$(COMMAND) "pip install tox && tox -e coverage"

clean:
	rm -rf build
	rm -rf limebet.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm -rf .tox
	rm -rf .cache
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -rf $(find . -type d -name __pycache__)
	rm .coverage
	rm .coverage.*

dockerclean:
	docker system prune -f
	docker system prune -f --volumes
