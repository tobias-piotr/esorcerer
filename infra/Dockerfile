FROM python:3.11.1-slim-buster as base

# Expose port
EXPOSE 80

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code"

# Install necessary soft
RUN apt-get update \
    && apt-get install -y netcat curl git make gcc postgresql python3-dev libpq-dev \
    && apt-get clean

# Local development
FROM base as dev

ENV DEVELOPMENT=1

# Copy & install dependencies
COPY ./requirements ./requirements
RUN pip install -r ./requirements/local.txt

COPY . .

CMD ["bash", "infra/run.sh"]

# Production environment
FROM base as prod

RUN useradd -mr esorcerer

USER esorcerer

ENV PATH=$PATH:/home/esorcerer/.local/bin

COPY --chown=esorcerer:esorcerer ./requirements ./requirements
RUN pip install -r ./requirements/prod.txt

COPY --chown=esorcerer:esorcerer . /code

CMD ["bash", "infra/run.sh"]
