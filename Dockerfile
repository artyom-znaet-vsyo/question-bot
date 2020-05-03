FROM python:3.8-slim

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN cd /app && poetry install --no-root

# Copy in everything else:
COPY question_bot /app/question_bot/
RUN poetry install

CMD poetry run questions_collector
