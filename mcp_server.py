from mcp.server.fastmcp import FastMCP
import asyncio
import logging
import datetime

logging.basicConfig(
    filename='/app/lab.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALLOWED_TARGETS = [
    'scanme.nmap.org',
    'localhost',
    '127.0.0.1',
    '172.18.0.3',
    '192.168.68.109'
]

mcp = FastMCP('kali-lab')

async def run_command(cmd, timeout=45):
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
        return stdout.decode() or stderr.decode() or 'No output'
    except asyncio.TimeoutError:
        proc.kill()
        return f'Scan timed out after {timeout} seconds'
    except Exception as e:
        return f'Error: {str(e)}'

@mcp.tool()
async def nmap_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    logging.info(f'nmap started on: {target} at {datetime.datetime.now()}')
    output = await run_command([
        'nmap', '-F', '--open', '-T4',
        '--max-retries', '1',
        '--host-timeout', '30s', target
    ])
    logging.info(f'nmap completed on: {target}')
    return output

@mcp.tool()
async def nikto_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    logging.info(f'nikto started on: {target} at {datetime.datetime.now()}')
    output = await run_command([
        'nikto', '-h', target, '-maxtime', '30'
    ])
    logging.info(f'nikto completed on: {target}')
    return output

@mcp.tool()
async def dirb_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    logging.info(f'dirb started on: {target} at {datetime.datetime.now()}')
    output = await run_command([
        'dirb', f'http://{target}',
        '/usr/share/dirb/wordlists/common.txt',
        '-S', '-r'
    ])
    logging.info(f'dirb completed on: {target}')
    return output

@mcp.tool()
async def sqlmap_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    logging.info(f'sqlmap started on: {target} at {datetime.datetime.now()}')
    output = await run_command([
        'sqlmap', '-u', f'http://{target}',
        '--batch', '--level', '1', '--risk', '1',
        '--timeout', '10', '--retries', '1'
    ], timeout=60)
    logging.info(f'sqlmap completed on: {target}')
    return output

@mcp.tool()
async def whatweb_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    logging.info(f'whatweb started on: {target} at {datetime.datetime.now()}')
    output = await run_command([
        'whatweb', '--no-errors', '-a', '1',
        f'http://{target}'
    ])
    logging.info(f'whatweb completed on: {target}')
    return output

@mcp.tool()
async def wafw00f_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    logging.info(f'wafw00f started on: {target} at {datetime.datetime.now()}')
    output = await run_command([
        'wafw00f', f'http://{target}'
    ])
    logging.info(f'wafw00f completed on: {target}')
    return output

@mcp.tool()
async def hydra_bruteforce(target: str, service: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    allowed_services = ['ssh', 'ftp', 'http-get']
    if service not in allowed_services:
        return f'Error: Service {service} not allowed. Use: ssh, ftp, http-get'
    logging.info(f'hydra started on: {target} service: {service} at {datetime.datetime.now()}')
    output = await run_command([
        'hydra', '-l', 'admin',
        '-P', '/usr/share/dirb/wordlists/common.txt',
        '-t', '4', '-f',
        target, service
    ], timeout=60)
    logging.info(f'hydra completed on: {target}')
    return output

if __name__ == '__main__':
    mcp.run(transport='stdio')
