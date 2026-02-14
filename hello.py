FROM python:3.11.11-slim-bookworm

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY common_lib /app/common_lib
COPY matcher/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY matcher/matcher.py .
COPY matcher/import_active.py .
COPY matcher/scheduler.py .

# Create cron job file
RUN echo "# Monthly wallet matching job" > /etc/cron.d/wallet-matcher
RUN echo "0 0 1 * * root cd /app && python matcher.py >> /var/log/matcher.log 2>&1" >> /etc/cron.d/wallet-matcher
RUN chmod 0644 /etc/cron.d/wallet-matcher
RUN crontab /etc/cron.d/wallet-matcher

# Create log file
RUN touch /var/log/matcher.log

CMD ["python", "scheduler.py"]