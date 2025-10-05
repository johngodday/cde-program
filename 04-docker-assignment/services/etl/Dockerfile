FROM python:3.10-slim

WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY . .

# Copy crontab file
COPY crontab.txt /etc/cron.d/weather-cron

# Set permissions
RUN chmod 0644 /etc/cron.d/weather-cron

# Apply the cron job
RUN crontab /etc/cron.d/weather-cron

# Start cron
CMD ["cron", "-f"]
