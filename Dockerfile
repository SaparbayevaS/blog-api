FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gettext \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirments ./requirments
RUN pip install --no-cache-dir -r requirments/base.txt

COPY . .

RUN useradd -m appuser
USER appuser

ENTRYPOINT ["bash", "scripts/entrypoint.sh"]