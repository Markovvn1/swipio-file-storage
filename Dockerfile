FROM markovvn1/python-poetry-docker:latest

ARG ENVIRONMENT='production'

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install $([ "$ENVIRONMENT" = 'production' ] && echo "--no-dev")

COPY file_storage file_storage

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "80", "file_storage:app"]
