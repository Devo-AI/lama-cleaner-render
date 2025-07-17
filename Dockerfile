FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git ffmpeg libsm6 libxext6 wget && \
    pip install --upgrade pip

COPY . .

RUN pip install lama-cleaner

EXPOSE 8080

CMD ["python3", "-m", "lama_cleaner", "--model", "lama", "--port", "8080", "--host", "0.0.0.0"]

