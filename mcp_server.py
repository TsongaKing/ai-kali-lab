from mcp.server.fastmcp import FastMCP
import asyncio
import logging
import datetime

ALLOWED_TARGETS = [
    'scanme.nmap.org',
    'localhost',
    '127.0.0.1',
    '172.18.0.2',
    '192.168.68.105'
]

mcp = FastMCP('kali-lab')

@mcp.tool()
async def nmap_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    proc = await asyncio.create_subprocess_exec(
        'nmap', '-F', '--open', '-T4', '--max-retries', '1', '--host-timeout', '30s', target,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=45)
    return stdout.decode() or stderr.decode() or 'No output'

@mcp.tool()
async def nikto_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    proc = await asyncio.create_subprocess_exec(
        'nikto', '-h', target, '-maxtime', '30',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=45)
    return stdout.decode() or stderr.decode() or 'No output'

@mcp.tool()
async def dirb_scan(target: str) -> str:
    if target not in ALLOWED_TARGETS:
        return f'Error: Target {target} not allowed'
    proc = await asyncio.create_subprocess_exec(
        'dirb', f'http://{target}', '/usr/share/dirb/wordlists/common.txt', '-S', '-r',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=45)
    return stdout.decode() or stderr.decode() or 'No output'

if __name__ == '__main__':
    mcp.run(transport='stdio')
