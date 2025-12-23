# Start from slim python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Prevent .pyc and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy and give permission to entrypoint
RUN chmod +x entrypoint.sh

# Expose Django port
EXPOSE 8080

# Start container with entrypoint
ENTRYPOINT ["./entrypoint.sh"]
