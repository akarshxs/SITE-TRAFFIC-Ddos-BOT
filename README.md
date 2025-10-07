# UltimateManu - Extreme Power Attack Tool

## ⚠️ **CRITICAL LEGAL AND ETHICAL WARNING**
This tool is **strictly for educational and authorized penetration testing purposes only**. It simulates high-volume network traffic and resource exhaustion techniques, which can be used to perform Distributed Denial of Service (DDoS) attacks. **Unauthorized use against any system, website, or network is illegal under laws such as the Computer Fraud and Abuse Act (CFAA) in the US, and similar regulations worldwide.** 

- **ONLY** use this on systems you own or have **explicit written permission** to test.
- Misuse can result in severe legal consequences, including fines and imprisonment.
- The developers and contributors bear no responsibility for illegal or unethical use.
- If you're learning about cybersecurity, consider ethical alternatives like CTF challenges, bug bounty programs, or tools like OWASP ZAP for authorized testing.

By using this tool, you agree to these terms and assume all risks.

## Overview
UltimateManu is an advanced Python-based stress testing tool designed to simulate extreme network loads on web servers. It includes features for bypassing common Web Application Firewalls (WAFs) like CloudFlare, resource exhaustion attacks, and stealthy traffic patterns. Built with modularity in mind, it supports multiple attack vectors to test server resilience under high pressure.

**Key Features:**
- **Multi-Threaded Attacks**: Up to 25,000+ threads for massive parallelism.
- **CloudFlare & WAF Bypass**: Mimics real browsers with fingerprinting, cookie handling, and header rotation.
- **Attack Modes**: Auto, Resource Exhaustion, Slow HTTP (Slowloris-style), Mixed, Super Effective, and Stealth modes.
- **Proxy & Tor Support**: Anonymity via proxies (from `proxies.txt`) or Tor network.
- **Target Monitoring**: Real-time status checks, response time tracking, and down detection.
- **Stealth Techniques**: Human-like browsing patterns to evade detection.
- **Socket-Level Control**: Direct TCP/SSL connections for low-level attacks like SSL renegotiation.

**Supported Protocols**: HTTP/HTTPS, with SSL/TLS handling.

## Requirements
- **Python**: 3.6+ (tested on 3.8-3.11)
- **Dependencies** (auto-installed if missing):
  - `requests`
  - `colorama`
  - `urllib3`
  - `pysocks` (for SOCKS proxies)
  - `stem` (for Tor control)
- **Tor** (optional): Install Tor and run it on port 9050 (SOCKS) and 9051 (control). No password by default.
- **Proxies** (optional): Free/public proxies in `proxies.txt` (formats: `http://ip:port`, `socks5://ip:port`).

### Installation
1. Clone or download the script (`ultimate_manu.py`).
2. Run: `python3 ultimate_manu.py`
   - The script will auto-install missing packages via pip.
3. (Optional) Create `proxies.txt` with your proxies (one per line).

**Note**: On Windows, ensure `pip` is in your PATH. For Tor, install from [torproject.org](https://www.torproject.org/).

## Usage
### Interactive Mode (Default)
Run the script without arguments for an interactive setup:
python3 ultimate_manu.py


Run
Copy code
- Enter target URL (e.g., `https://example.com`).
- Configure threads, proxies, Tor, CloudFlare bypass, and attack mode.
- Press Ctrl+C to stop.

### Command-Line Arguments
python3 ultimate_manu.py -u <URL> -t <threads> -p -c


Run
Copy code
- `-u, --url`: Target URL (e.g., `https://example.com`).
- `-t, --threads`: Number of threads (default: 25000).
- `-p, --proxy`: Enable proxy usage from `proxies.txt`.
- `-c, --cloudflare`: Enable CloudFlare bypass.

**Example**:
python3 ultimate_manu.py -u https://test-site.com -t 5000 -p -c


Run
Copy code

### Attack Modes
Select during interactive setup or via code modification:
1. **Auto** (default): Balanced mix of all techniques.
2. **Resource**: CPU/RAM exhaustion via complex requests and large payloads.
3. **Slow**: Connection pool exhaustion (Slowloris, Slow POST, Slow Read).
4. **Mixed**: Even distribution across all modes.
5. **Super Effective** (advanced): Combines TCP exhaustion, SSL renegotiation, and memory floods.
6. **Stealth**: Undetectable browsing simulation with human-like patterns.

### Configuration Files
- **`proxies.txt`**: List proxies (auto-created if missing). Example:
HTTP Proxy
http://123.45.67.89:8080

SOCKS5 with auth
socks5://user:pass@98.76.54.32:1080


Run
Copy code
- **Tor Setup**: Edit `tor_control_port` and `tor_password` in the script if needed.

## How It Works
1. **Setup**: Parses target URL, loads proxies/Tor, and configures bypass techniques.
2. **Bypass Phase**: Obtains CloudFlare cookies and applies WAF evasion (headers, IPs, timing).
3. **Attack Launch**: Spawns threads in selected mode(s):
 - **HTTP Workers**: Flood with GET/POST requests using rotated UAs and fingerprints.
 - **Socket Workers**: Direct TCP/SSL connections for raw flooding.
 - **Resource Exhaustion**: Complex JSON payloads and admin path queries to spike CPU/RAM.
 - **Slow HTTP**: Holds connections open to exhaust server pools.
 - **Stealth**: Simulates user sessions with reading/thinking delays.
4. **Monitoring**: Tracks RPS, success rate, response times, and detects if target is "down" (e.g., 500+ errors or timeouts).
5. **Cleanup**: Closes connections and shows stats on stop.

**Output Example**:
[+] Target: UP | Requests: 1,234,567 | RPS: 12,345.67 | Success: 98.5% | Resp Time: 0.12s | Time: 100.0s [!] TARGET IS DOWN! Reason: Multiple connection timeouts


Run
Copy code

## Advanced Features
- **Browser Fingerprinting**: Realistic UAs, sec-ch-ua headers, and screen resolutions.
- **IP Spoofing**: X-Forwarded-For, CF-Connecting-IP for CDN bypass.
- **SSL Resource Exhaustion**: Renegotiation attacks (if server allows).
- **Anti-Detection**: Random delays, referrer rotation, and session consistency.
- **Bulletproof Hosting Counter**: Targets resilient servers with mixed vectors.

## Troubleshooting
- **Import Errors**: Run `pip install -r requirements.txt` (create if needed) or let the script auto-install.
- **Proxy Issues**: Test proxies manually (e.g., via `curl`). Invalid proxies cause failures.
- **Tor Errors**: Ensure Tor is running (`tor` command). Check control port authentication.
- **High Local CPU/Memory**: Reduce threads (e.g., `-t 1000`) or run on a VPS.
- **Firewall Blocks**: Enable bypass (`-c`) or use more proxies/Tor.
- **Target Not Down**: Increase threads/duration, or switch modes (e.g., Slow for connection-limited servers).
- **Legal Blocks**: If your ISP blocks ports, use Tor or VPN.

**Common Errors**:
- `ConnectionError`: Target down, firewall, or network issue.
- `ProxyError`: Bad proxy; rotate or add more to `proxies.txt`.
- `SSL Errors`: Disable verification (already set) or use HTTP target.

## Limitations
- **Not Truly Distributed**: Single-machine; for real DDoS, use botnets (illegal!).
- **Detection Risk**: Even stealth mode can be flagged by advanced WAFs (e.g., Akamai, Imperva).
- **Resource Intensive**: Requires a powerful machine (8+ GB RAM, multi-core CPU).
- **Tor Speed**: Slows attacks; use for anonymity only.
- **No GUI**: CLI-only; extend with Tkinter if needed.

## Contributing & Support
- **Educational Use**: Fork for learning; contribute ethical improvements (e.g., better monitoring).
- **Issues**: Report bugs on GitHub (if hosted); include Python version and error logs.
- **Alternatives**: For legit testing, use `Apache Benchmark (ab)`, `Locust`, or `JMeter`.

## License
MIT License - See `LICENSE` file (or create one). Copyright © 2024 SHAHxKNIGHT CREW. Unauthorized distribution/modification prohibited for malicious intent.

**Remember: With great power comes great responsibility. Use ethically!** 🚀
