FROM python:3.12-slim

WORKDIR /app

COPY validate.py .
COPY shards/ /shards/

ENTRYPOINT ["python", "validate.py"]
