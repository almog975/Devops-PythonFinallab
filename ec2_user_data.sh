#!/bin/bash
# ── EC2 User Data: Install Docker, pull image, run Lab Monitor ────────────────
# Works on: Amazon Linux 2023 / Ubuntu 22.04 LTS
# Exposes the webapp on TCP port 2468 (mapped to container port 80)
# Replace <YOUR_DOCKERHUB_USERNAME> with your actual Docker Hub username

set -e

# ── Detect OS and install Docker ─────────────────────────────────────────────
if command -v dnf &>/dev/null; then
    # Amazon Linux 2023
    dnf update -y
    dnf install -y docker
    systemctl enable --now docker
else
    # Ubuntu
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io
    systemctl enable --now docker
fi

# ── Pull image from Docker Hub ────────────────────────────────────────────────
docker pull <YOUR_DOCKERHUB_USERNAME>/lab-monitor:latest

# ── Run the container ─────────────────────────────────────────────────────────
# -p 2468:80   → expose on EIP:2468
# -v lab-data:/data → named volume for persistent data
# --restart unless-stopped → survive reboots
docker volume create lab-data

docker run -d \
    --name lab-monitor \
    -p 2468:80 \
    -v lab-data:/data \
    --restart unless-stopped \
    <YOUR_DOCKERHUB_USERNAME>/lab-monitor:latest
