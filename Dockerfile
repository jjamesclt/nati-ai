#FROM nvcr.io/nvidia/pytorch:23.09-py3
#FROM jjamesclt/pytorch23:base
#FROM jjamesclt/nati-pytorch-base:23.09
#FROM nvcr.io/nvidia/pytorch:22.12-py3
FROM nvcr.io/nvidia/pytorch:22.04-py3

WORKDIR /app

# Optional: install tools (uncomment if transformers/git fail)
# RUN apt-get update && apt-get install -y git curl

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
