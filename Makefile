build:
	DOCKER_BUILDKIT=1 docker build --tag projects-api:latest --target projects-api .

run:
	docker compose up -d