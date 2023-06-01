FROM python:3.11.3-slim-bullseye

RUN mkdir -p /app
WORKDIR /app


ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-directory

COPY . .
RUN poetry install --no-dev
RUN poetry run download

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]