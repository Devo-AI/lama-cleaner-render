FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Clone lama-cleaner source code
RUN git clone https://github.com/Sanster/lama-cleaner.git . && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# Expose port for Render
EXPOSE 8080

# Launch lama-cleaner in CPU mode
CMD ["python3", "-m", "lama_cleaner", "--model", "lama", "--host", "0.0.0.0", "--port", "8080", "--device", "cpu"]
