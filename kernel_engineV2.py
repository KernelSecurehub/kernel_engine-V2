#!/usr/bin/env python3
"""
KERNEL Engine v2.0 - Fully Automated Penetration Testing & Recon Framework
Developed by: KERNEL Secure Hub (mohamro32@gmail.com)
Usage: python3 kernel_engine.py -t target.com
"""

import asyncio
import argparse
import json
import socket
import sys
from datetime import datetime
import aiohttp
import requests

BANNER = """
\033[92m
  _  ________ _____  _  ________ _       ______ _   _  _____ _____ _          ______ 
 | |/ /  ____|  __ \| |/ /  ____| |     |  ____| \ | |/ ____|_   _| \ | |  ____|  ____|
 | ' /| |__  | |__) | ' /| |__  | |     | |__  |  \| | |  __  | | |  \| | |__  | |__   
 |  < |  __| |  _  /|  < |  __| | |     |  __| | . ` | | |_ | | | | . ` |  __| |  __|  
 | . \| |____| | \ \| . \| |____| |____ | |____| |\  | |__| |_| |_| |\  | |____| |____ 
 |_|\_\______|_|  \_\_|\_\______|______||______|_| \_|\_____|_____|_| \_|______|______|
                                                                                       
 [ FULLY AUTOMATED RECON & VULNERABILITY ENGINE | KERNEL SECURE HUB ]
\033[0m"""

SENSITIVE_PATHS = [
    "/.env", "/.git/HEAD", "/robots.txt", "/config.php",
    "/wp-config.php.bak", "/admin/", "/phpmyadmin/"
]

SECURITY_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy",
    "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
]

COMMON_PORTS = [21, 22, 80, 443, 3306, 8080, 8443]

class KernelEngine:
    def __init__(self, target):
        self.target = target.replace("http://", "").replace("https://", "").strip("/")
        self.results = {
            "target": self.target,
            "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "ip": None,
            "subdomains": [],
            "open_ports": [],
            "missing_headers": [],
            "exposed_files": [],
            "risk_score": 0
        }

    async def resolve_ip(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.results["ip"] = ip
            print(f"\033[92m[+] IP Resolved: {ip}\033[0m")
        except Exception:
            print("\033[91m[-] Failed to resolve IP\033[0m")

    def fetch_subdomains(self):
        print("\033[94m[*] Enumerating Subdomains via SSL Transparency logs...\033[0m")
        url = f"https://crt.sh/?q=%.{self.target}&output=json"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                subs = set()
                for item in res.json():
                    name = item['name_value']
                    for sub in name.split('\n'):
                        if self.target in sub and not sub.startswith('*'):
                            subs.add(sub.strip())
                self.results["subdomains"] = list(subs)
                print(f"\033[92m[+] Found {len(subs)} Subdomains\033[0m")
        except Exception as e:
            print(f"\033[93m[!] Subdomain fetch failed: {e}\033[0m")

    async def scan_port(self, port):
        conn = asyncio.open_connection(self.results["ip"], port)
        try:
            _, writer = await asyncio.wait_for(conn, timeout=1.5)
            self.results["open_ports"].append(port)
            print(f"\033[92m[+] Port Open: {port}\033[0m")
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    async def scan_ports(self):
        if not self.results["ip"]:
            return
        print("\033[94m[*] Scanning Critical Network Ports...\033[0m")
        tasks = [self.scan_port(p) for p in COMMON_PORTS]
        await asyncio.gather(*tasks)

    async def audit_web(self):
        print("\033[94m[*] Auditing Web Headers & Sensitive Files...\033[0m")
        base_url = f"https://{self.target}"
        async with aiohttp.ClientSession() as session:
            # 1. Header Check
            try:
                async with session.get(base_url, timeout=5, ssl=False) as res:
                    headers = res.headers
                    for h in SECURITY_HEADERS:
                        if h not in headers:
                            self.results["missing_headers"].append(h)
            except Exception:
                pass

            # 2. Sensitive Files Check
            for path in SENSITIVE_PATHS:
                try:
                    async with session.get(f"{base_url}{path}", timeout=3, ssl=False) as res:
                        if res.status == 200:
                            print(f"\033[91m[!] EXPOSED FILE FOUND: {path}\033[0m")
                            self.results["exposed_files"].append(path)
                except Exception:
                    pass

    def calculate_risk(self):
        score = 0
        score += len(self.results["missing_headers"]) * 5
        score += len(self.results["exposed_files"]) * 25
        score += len(self.results["open_ports"]) * 10
        self.results["risk_score"] = min(score, 100)

    def generate_html_report(self):
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>KERNEL Security Audit - {self.target}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }}
                .card {{ background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .score {{ font-size: 32px; font-weight: bold; color: {'#ef4444' if self.results['risk_score'] > 40 else '#10b981'}; }}
                h1, h2 {{ color: #34d399; }}
                ul {{ line-height: 1.8; }}
            </style>
        </head>
        <body>
            <h1>KERNEL Secure Hub - Security Report</h1>
            <div class="card">
                <h2>Target: {self.target} ({self.results['ip']})</h2>
                <p>Date: {self.results['timestamp']}</p>
                <p>Overall Threat Score: <span class="score">{self.results['risk_score']}%</span></p>
            </div>
            <div class="card">
                <h3>Discovered Subdomains ({len(self.results['subdomains'])})</h3>
                <ul>{"".join([f"<li>{s}</li>" for s in self.results['subdomains']]) or "None"}</ul>
            </div>
            <div class="card">
                <h3>Exposed Sensitive Files</h3>
                <ul>{"".join([f"<li style='color:#ef4444'>{f}</li>" for f in self.results['exposed_files']]) or "None"}</ul>
            </div>
            <div class="card">
                <h3>Open Ports</h3>
                <p>{", ".join(map(str, self.results['open_ports'])) or "None"}</p>
            </div>
        </body>
        </html>
        """
        filename = f"KERNEL_Report_{self.target}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n\033[92m[✔] FULL HTML REPORT GENERATED: {filename}\033[0m")

    async def run(self):
        print(BANNER)
        print(f"\033[95m[🚀] LAUNCHING FULL AUTOMATED SCAN FOR: {self.target}\033[0m\n")
        await self.resolve_ip()
        self.fetch_subdomains()
        await self.scan_ports()
        await self.audit_web()
        self.calculate_risk()
        self.generate_html_report()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KERNEL Fully Automated Security Engine")
    parser.add_argument("-t", "--target", required=True, help="Target domain (e.g. target.com)")
    args = parser.parse_args()

    engine = KernelEngine(args.target)
    asyncio.run(engine.run())
