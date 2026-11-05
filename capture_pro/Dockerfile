FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    ocrmypdf tesseract-ocr tesseract-ocr-por ghostscript default-jre \
    && rm -rf /var/lib/apt/lists/*
# veraPDF requires a separately verified distribution/license and installer.
# Build intentionally does NOT start a worker without that dependency installed.
WORKDIR /app
COPY capture_pro/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY capture_pro/ /app/capture_pro/
CMD ["python","-m","capture_pro.worker"]
