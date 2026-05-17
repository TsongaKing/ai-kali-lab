# AI-Powered Security Lab - MCP + Docker + Ubuntu
![CI - Security Lab](https://github.com/TsongaKing/ai-kali-lab/actions/workflows/ci.yml/badge.svg)

A professional, containerised security lab that connects Claude AI to real security tools via the Model Context Protocol (MCP). Built for ethical hacking practice, DevSecOps learning, and security automation research.

## Architecture

AI Assistant (Claude Desktop)
     |
     MCP via docker exec
     |
MCP Server (Ubuntu 24.04)
     |-- nmap        - network and port scanning
     |-- nikto       - web vulnerability scanning
     |-- dirb        - directory enumeration
     |-- sqlmap      - SQL injection detection
     |-- whatweb     - web technology fingerprinting
     |-- wafw00f     - WAF detection
     |-- hydra       - password brute forcing
     |
     isolated lab-network
     |
     DVWA (PHP 8.5 + Apache 2.4.67) - legal practice target
     MariaDB 10                      - database backend

## Features

- 7 security tools accessible directly from Claude Desktop via MCP
- Safety controls - target whitelisting, all scans restricted to approved hosts only
- Audit logging - every tool call logged with timestamps to lab.log
- Docker isolation - all containers run on an isolated bridge network
- Capability restrictions - cap_drop ALL with only NET_RAW and NET_ADMIN added back
- DVWA - Damn Vulnerable Web Application for legal hands-on practice
- Security hardening applied to DVWA: security headers, version disclosure removed, HttpOnly cookies

## Prerequisites

- Docker Desktop
- Claude Desktop

## Quick Start

### 1. Clone the repository

git clone https://github.com/TsongaKing/ai-kali-lab.git
cd ai-kali-lab

### 2. Build and start all containers

docker-compose up --build -d

This starts three containers:
- ai-kali-lab-mcp-server-1 - security tools on port 8000
- ai-kali-lab-dvwa-1 - DVWA on port 8080
- ai-kali-lab-db-1 - MariaDB database

### 3. Set up DVWA

1. Go to http://localhost:8080
2. Log in with admin / password
3. Click Create / Reset Database
4. Log in again

### 4. Connect to Claude Desktop

Edit your Claude Desktop config (Settings - Developer - Edit Config):

{
  "mcpServers": {
    "kali-lab": {
      "command": "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe",
      "args": ["exec", "-i", "ai-kali-lab-mcp-server-1", "bash", "/app/run_mcp.sh"]
    }
  }
}

### 5. Restart Claude Desktop

kali-lab will show as running under Settings - Developer. You can now ask Claude to run security scans directly from chat.

## Available Tools

| Tool | Description |
|------|-------------|
| nmap_scan | Network and port scanning |
| nikto_scan | Web server vulnerability scanning |
| dirb_scan | Directory and file enumeration |
| sqlmap_scan | SQL injection detection |
| whatweb_scan | Web technology fingerprinting |
| wafw00f_scan | WAF detection |
| hydra_bruteforce | Password brute forcing |

## Approved Targets

All tools are restricted to this whitelist only:

- scanme.nmap.org (Nmap official test server)
- localhost / 127.0.0.1
- 172.18.0.3 (DVWA container)

To add your own lab target, add its IP to ALLOWED_TARGETS in mcp_server.py and copy to the container:

docker cp mcp_server.py ai-kali-lab-mcp-server-1:/app/mcp_server.py
docker-compose restart mcp-server

## Project Structure

- Dockerfile              - Ubuntu 24.04 + all security tools
- docker-compose.yml      - MCP server + DVWA + MariaDB
- mcp_server.py           - MCP server with 7 tools and safety controls
- server.py               - FastAPI HTTP server
- run_mcp.sh              - Bash wrapper for MCP stdio transport
- requirements.txt        - Python dependencies
- README.md

## Security Controls

| Control | Implementation |
|---------|----------------|
| Target whitelisting | All tools validate against ALLOWED_TARGETS |
| Audit logging | Every tool call logged with timestamp |
| Network isolation | Containers on isolated lab-network bridge |
| Capability dropping | cap_drop ALL - only NET_RAW and NET_ADMIN added |
| No arbitrary shell | Only predefined tool functions exposed |

## DVWA Security Hardening Applied

| Finding | Fix |
|---------|-----|
| Missing X-Frame-Options | Header always set X-Frame-Options DENY |
| Missing X-Content-Type-Options | Header always set X-Content-Type-Options nosniff |
| Server version disclosure | ServerTokens Prod + ServerSignature Off |
| PHP version disclosure | Header unset X-Powered-By |
| HttpOnly cookies missing | session.cookie_httponly = 1 |
| ETag inode leakage | FileETag None |

## Useful Commands

Start everything:        docker-compose up -d
Stop everything:         docker-compose down
Rebuild after changes:   docker-compose up --build -d
View audit logs:         docker exec ai-kali-lab-mcp-server-1 cat /app/lab.log
Get DVWA IP:             docker inspect ai-kali-lab-dvwa-1 | grep IPAddress

## Tech Stack

Docker, Docker Compose, Ubuntu 24.04, Python, FastMCP, FastAPI, Uvicorn,
nmap, nikto, dirb, sqlmap, hydra, whatweb, wafw00f, DVWA, MariaDB, Claude Desktop

## Legal

This lab is for educational purposes only.
Only scan systems you own or have explicit written permission to test.
Unauthorized scanning is illegal in most jurisdictions.

Built by @TsongaKing
