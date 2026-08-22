FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY mcp_server ./mcp_server

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('BAAI/bge-base-en-v1.5')"

CMD ["python", "-m", "mcp_server.server"]