FROM python:3.9.21

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-fastsam.txt .
COPY requirements-api.txt .

RUN --mount=type=cache,target=/root/.cache/pip,id=pip_fastsam_api \
    pip install --upgrade pip && \
    pip install -r requirements-fastsam.txt && \
    pip install -r requirements-api.txt

COPY fastsam/ ./fastsam/
COPY assets/ ./assets/
COPY ultralytics/ ./ultralytics/
COPY utils/ ./utils/
COPY api.py .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
