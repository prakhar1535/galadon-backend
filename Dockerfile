FROM python:3.11-slim

# Disable Python bytecode and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy application code to container
COPY . /app

# Make the gunicorn.sh script executable
RUN chmod +x /app/gunicorn.sh

# Copy the .env file and make the environment variables available
COPY .env /app/.env
ENV $(cat /app/.env | grep -v '^#' | xargs)

# Create a non-root user to run the application
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port on which the application will run
EXPOSE 8000

# Run the Gunicorn script
CMD ["/app/gunicorn.sh"]

