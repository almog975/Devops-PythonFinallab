# ── Lab Monitor – Docker Mission ──────────────────────────────────────────────
# Base image: Ubuntu LTS
FROM ubuntu:22.04

# Prevent interactive prompts during apt
ENV DEBIAN_FRONTEND=noninteractive

# ── 1. Install nginx (webserver) + curl + aws cli (to fetch from S3) ──────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        curl \
        unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
    && unzip /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/awscliv2.zip /tmp/aws \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── 2. Download the webapp from GitHub ───────────────────────────────────────
RUN curl -fsSL \
    "https://raw.githubusercontent.com/almog975/Devops-PythonFinallab/main/LabManager.html" \
    -o /var/www/html/index.html

# ── 3. Download dummy data from S3 to a temp location ────────────────────────
# Replace the URL below with your actual S3 public URL
ARG S3_DATA_URL=https://YOUR-BUCKET.s3.amazonaws.com/lab_data.json
RUN curl -fsSL "${S3_DATA_URL}" -o /tmp/lab_data.json

# ── 4. Nginx config – serve /data/ from the mounted volume ───────────────────
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d/labmonitor.conf

# ── 5. Declare the data volume (app reads/writes JSON here) ──────────────────
VOLUME ["/data"]

# ── 6. Expose port 80 ────────────────────────────────────────────────────────
EXPOSE 80

# ── 7. Entrypoint: move dummy data → volume, erase temp, start nginx ─────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
