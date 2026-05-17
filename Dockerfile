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
    libcap2-bin \
    && apt clean

RUN groupadd -r mcp && useradd -r -g mcp -m mcp

RUN setcap cap_net_raw,cap_net_admin+eip /usr/bin/nmap

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages

COPY . .

RUN chown -R mcp:mcp /app

USER mcp

CMD python3 -m uvicorn server:app --host 0.0.0.0 --port 8000
