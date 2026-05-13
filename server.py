from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import logging
import datetime

# Logging setup - records everything that happens
logging.basicConfig(
    filename='lab.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Only these targets are allowed - no arbitrary scanning
ALLOWED_TARGETS = [
    'scanme.nmap.org',
    'localhost',
    '127.0.0.1',
    'dvwa'
]

class ScanRequest(BaseModel):
    target: str

class NiktoRequest(BaseModel):
    target: str

class GobusterRequest(BaseModel):
    target: str

@app.get('/')
def home():
    logging.info('Health check called')
    return {'status': 'running', 'time': str(datetime.datetime.now())}

@app.post('/scan')
def scan(req: ScanRequest):
    if req.target not in ALLOWED_TARGETS:
        logging.warning(f'Blocked scan attempt on unauthorized target: {req.target}')
        raise HTTPException(status_code=403, detail='Target not allowed')

    logging.info(f'Nmap scan started on approved target: {req.target}')

    result = subprocess.run(
        ['nmap', '-F', '--open', req.target],
        capture_output=True,
        text=True,
        timeout=120
    )

    logging.info(f'Nmap scan completed on: {req.target}')
    return {
        'tool': 'nmap',
        'target': req.target,
        'output': result.stdout,
        'timestamp': str(datetime.datetime.now())
    }

@app.post('/nikto')
def nikto(req: NiktoRequest):
    if req.target not in ALLOWED_TARGETS:
        logging.warning(f'Blocked nikto attempt on unauthorized target: {req.target}')
        raise HTTPException(status_code=403, detail='Target not allowed')

    logging.info(f'Nikto scan started on approved target: {req.target}')

    result = subprocess.run(
        ['nikto', '-h', req.target, '-maxtime', '60'],
        capture_output=True,
        text=True,
        timeout=120
    )

    logging.info(f'Nikto scan completed on: {req.target}')
    return {
        'tool': 'nikto',
        'target': req.target,
        'output': result.stdout,
        'timestamp': str(datetime.datetime.now())
    }

@app.post('/gobuster')
def gobuster(req: GobusterRequest):
    if req.target not in ALLOWED_TARGETS:
        logging.warning(f'Blocked gobuster attempt on unauthorized target: {req.target}')
        raise HTTPException(status_code=403, detail='Target not allowed')

    logging.info(f'Gobuster scan started on approved target: {req.target}')

    result = subprocess.run(
        ['gobuster', 'dir',
         '-u', f'http://{req.target}',
         '-w', '/usr/share/wordlists/dirb/common.txt',
         '--timeout', '10s'],
        capture_output=True,
        text=True,
        timeout=120
    )

    logging.info(f'Gobuster scan completed on: {req.target}')
    return {
        'tool': 'gobuster',
        'target': req.target,
        'output': result.stdout,
        'timestamp': str(datetime.datetime.now())
    }
