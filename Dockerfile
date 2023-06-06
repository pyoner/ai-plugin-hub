FROM python:3.11.3-slim-bullseye as builder


RUN mkdir -p /builder
WORKDIR /builder


COPY . .
RUN --mount=type=cache,target=/root/.cache pip3 install poetry

# projects api
COPY poetry.toml projects/api
RUN --mount=type=cache,target=/root/.cache poetry install -C projects/api

# RUN poetry build -f wheel
# RUN poetry export -f requirements.txt -o requirements.txt --without-hashes
# RUN pip wheel -r requirements.txt -w ./dist

# final stage
FROM python:3.11.3-slim-bullseye as projects-api

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY --from=builder /builder/projects/api /app

EXPOSE 8080
CMD [".venv/bin/python", "-m", "uvicorn", "src.projects.api.main:app", "--host", "0.0.0.0", "--port", "8080"]