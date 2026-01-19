FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# FFMPEG is crucial for moviepy
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
