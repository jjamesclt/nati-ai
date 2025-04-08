FROM nvcr.io/nvidia/pytorch:23.09-py3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY config/ ./config

ENV PYTHONUNBUFFERED=1
CMD ["python", "app/main.py"]
