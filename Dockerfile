FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN chmod +x /app/gunicorn.sh
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000

CMD ["/app/gunicorn.sh"]
