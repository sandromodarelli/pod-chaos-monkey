FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/. .

CMD ["python", "main.py"]
