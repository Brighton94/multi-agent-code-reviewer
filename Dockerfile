FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install

RUN curl -fsSL https://ollama.com/install.sh | sh

ENTRYPOINT [ "bash" ]