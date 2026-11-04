FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-por && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements-ai.txt .
RUN pip install --no-cache-dir -r requirements-ai.txt
COPY arquindex_ai_app.py .
EXPOSE 8000
CMD ["sh","-c","uvicorn arquindex_ai_app:app --host 0.0.0.0 --port ${PORT:-8000}"]
