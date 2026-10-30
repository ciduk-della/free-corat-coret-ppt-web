FROM python:3.11-slim

# Install system dependencies & headless LibreOffice for server-side PPTX conversion
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-nogui \
    libreoffice-impress \
    fonts-dejavu \
    fonts-liberation \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install Python libraries and gunicorn WSGI server
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy all application source code
COPY . .

# Ensure storage directories exist with write permissions
RUN mkdir -p uploads projects exports static/vendor

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose web port
EXPOSE 5000

# Run with Gunicorn WSGI production server
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 --access-logfile - 'app:create_app()'"]

