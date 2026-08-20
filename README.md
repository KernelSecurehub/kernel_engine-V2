# ⚡ KERNEL Engine (v2.0)

> **Fully Automated Penetration Testing & Reconnaissance Framework** developed by **KERNEL Secure Hub**.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Async Engine](https://img.shields.io/badge/architecture-asyncio-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Category](https://img.shields.io/badge/category-Cyber%20Security%20%26%20Pentesting-red)
![Maintainer](https://img.shields.io/badge/maintainer-KERNEL%20Secure%20Hub-111827)

---

## 📌 Overview

**KERNEL Engine v2.0** is an automated, high-performance security auditing and threat intelligence framework designed for security engineers, system administrators, and red teams. 

Unlike basic scanners, **KERNEL Engine** executes a full-spectrum security assessment using asynchronous IO (`asyncio`), discovers exposed sensitive assets, calculates a dynamic **Risk Score (0–100%)**, and automatically generates an enterprise-ready **HTML Security Audit Report** in seconds.

---

## ✨ Automated Scanning Modules

* 🌐 **DNS & Network Mapping**: Resolves target IPv4 addresses and verifies network responsiveness.
* 🔍 **Subdomain Enumeration**: Queries passive Certificate Transparency logs (`crt.sh`) to map subdomains without sending intrusive packets.
* 🚀 **Async Port Scanner**: Fast concurrent port scanning powered by Python’s `asyncio` engine.
* 🛡️ **Security Headers Audit**: Checks web application compliance against standard OWASP security headers (`HSTS`, `CSP`, `X-Frame-Options`, `X-Content-Type-Options`).
* 🚨 **Exposed Sensitive Files Detector**: Uncovers critical server leaks (`.env`, `.git/HEAD`, `wp-config.php`, `/admin/`).
* 📊 **Dynamic Risk Scoring Engine**: Calculates an automated risk percentage based on vulnerability severity.
* 📑 **Branded HTML Report Generator**: Exports a styled, client-ready HTML security report featuring KERNEL branding.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python **3.10+**
* `pip` package manager

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/KernelSecurehub/kernel_engineV2.git
# 2. Navigate to the project directory
cd kernel-engine

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Grant execution permissions (Linux/macOS)
chmod +x kernel_engine.py
