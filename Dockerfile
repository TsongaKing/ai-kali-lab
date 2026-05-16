FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    nmap \
    nikto \
    gobuster \
    dirb \
    sqlmap \
    hydra \
    whatweb \
    wafw00f \
    curl \
    git \
    net-tools \
    dnsutils \
    iputils-ping \
    && apt clean

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages

COPY . .

CMD python3 -m uvicorn server:app --host 0.0.0.0 --port 8000
