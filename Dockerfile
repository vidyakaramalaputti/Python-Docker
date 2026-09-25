FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import fastapi, uvicorn; print('Deps OK:', fastapi.__version__, uvicorn.__version__)"

COPY app.py .


RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser


EXPOSE 8000


CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 

