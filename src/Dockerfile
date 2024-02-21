FROM python:3.10

WORKDIR backend/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry && \
       poetry config virtualenvs.create false && \
       poetry install --no-interaction --no-ansi
