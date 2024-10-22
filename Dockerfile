FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry install

RUN curl -fsSL https://ollama.com/install.sh | sh

CMD ["sleep", "infinity"]