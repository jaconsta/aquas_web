PORT?=8000

DOCKER_IMAGE?=pomelo
DOCKER_CONTAINER?=${DOCKER_IMAGE}_dev

run-local:
	python aquas_web/manage.py runserver 0.0.0.0:8000
build:
	docker build . -t ${DOCKER_IMAGE}
run: build
	docker run -d -p 8000:8000 --name=${DOCKER_CONTAINER} ${DOCKER_IMAGE}
stop:
	docker container stop ${DOCKER_CONTAINER}
delete-container: stop
	docker rm ${DOCKER_CONTAINER}
delete: delete-container
	docker rmi ${DOCKER_IMAGE}
compose-dev:
	docker-compose -f config/compose/compose-dev.yml up --abort-on-container-exit

logs:
	docker logs -f ${DOCKER_CONTAINER}
