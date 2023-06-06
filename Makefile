build:
	DOCKER_BUILDKIT=1 docker build --tag projects-api:latest --target projects-api .

run:
	docker run -p 8000:8000 projects-api