FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir "docling-serve[ui]"

EXPOSE 8000

CMD ["docling-serve", "ui", "--host", "0.0.0.0", "--port", "8000"]