# Build image
FROM python:3.13-bookworm AS builder


RUN apt update
RUN apt install postgresql-client -y

ARG POETRY_VERSION="2.1.1"
RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY utils/ utils

# Poetry complains without a readme
RUN touch README.md
RUN poetry install --no-root

COPY src ./src
RUN poetry install

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
