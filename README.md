# AI Kali Linux MCP Lab

A controlled, isolated security learning environment using Docker and MCP.

## Purpose
- Learn cybersecurity tools safely
- Practice against intentionally vulnerable targets
- Understand AI tool orchestration
- DevSecOps experimentation

## Architecture
AI Assistant -> MCP Server (port 8000) -> Kali Linux Container -> Approved Targets
                                       -> DVWA (port 8080)

## Quick Start

### Build and Start Everything
docker-compose up --build

### Stop Everything
docker-compose down

### View Logs
type lab.log

## Approved Targets
- scanme.nmap.org (Nmap's official test target)
- localhost
- 127.0.0.1
- DVWA at http://localhost:8080

## Safety Rules
- Never scan targets you do not own or have permission to test
- All actions are logged to lab.log with timestamps
- Unauthorized targets are blocked and logged automatically
- Container is isolated from your main system via lab-network

## Project Structure
- Dockerfile        -> builds the Kali Linux container
- server.py         -> MCP server with safety controls
- docker-compose.yml -> spins up all containers together
- requirements.txt  -> Python dependencies
- .env              -> configuration settings
- lab.log           -> auto-generated activity log

## Legal
This lab is for educational purposes only.
Only test against systems you own or have explicit written permission to test.
