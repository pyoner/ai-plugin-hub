FROM python:3.11.3-slim-bullseye as builder

WORKDIR /builder
RUN --mount=type=cache,target=/root/.cache pip3 install poetry

# libs
COPY libs .
# projects api
COPY poetry.toml projects/api/pyproject.toml projects/api/
RUN --mount=type=cache,target=/root/.cache poetry install -C projects/api
COPY projects/api ./projects/




# runtime
FROM python:3.11.3-slim-bullseye as projects-api

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY --from=builder /builder/projects/api /app

EXPOSE 8080
CMD ["python", "-m", "uvicorn", "src.projects.api.main:app", "--host", "0.0.0.0", "--port", "8080"]