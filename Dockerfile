# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (needed for some Python deps)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    export PATH="/root/.cargo/bin:$PATH"

ENV PATH="/root/.cargo/bin:$PATH"

# Install Lama-Cleaner
RUN pip install --upgrade pip && \
    pip install lama-cleaner

FROM lama-cleaner/lama-cleaner:latest

# Set default command
CMD ["python3", "-m", "lama_cleaner", "--model", "lama", "--host", "0.0.0.0", "--port", "8080", "--device", "cpu"]

EXPOSE 8080
