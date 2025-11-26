import requests
import urllib3
from rich.console import Console

# Disable warnings for self-signed certs if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

class HTTPClient:
    def __init__(self, proxy=None, cookies=None, headers=None, timeout=10, verbose=False):
        self.session = requests.Session()
        self.timeout = timeout
        self.verbose = verbose
        
        # Set User-Agent
        self.session.headers.update({
            "User-Agent": "Cerberus-FUEF/1.0 (Security Testing)"
        })

        # Configure Proxy
        if proxy:
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }
            if self.verbose:
                console.print(f"[dim][*] Proxy set to {proxy}[/dim]")

        # Configure Cookies
        if cookies:
            # Parse cookie string "key=value; key2=value2"
            cookie_dict = {}
            for pair in cookies.split(';'):
                if '=' in pair:
                    key, value = pair.strip().split('=', 1)
                    cookie_dict[key] = value
            self.session.cookies.update(cookie_dict)
            if self.verbose:
                console.print(f"[dim][*] Cookies loaded: {len(cookie_dict)}[/dim]")

        # Configure Headers
        if headers:
            for header in headers:
                if ':' in header:
                    key, value = header.split(':', 1)
                    self.session.headers.update({key.strip(): value.strip()})
            if self.verbose:
                console.print(f"[dim][*] Custom headers loaded: {len(headers)}[/dim]")

    def get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def _request(self, method, url, **kwargs):
        try:
            if self.verbose:
                console.print(f"[dim] -> {method} {url}[/dim]")
            
            response = self.session.request(method, url, timeout=self.timeout, verify=False, **kwargs)
            
            if self.verbose:
                status_color = "green" if response.status_code < 400 else "red"
                console.print(f"[dim] <- {response.status_code} [{len(response.content)} bytes][/dim]")
            
            return response
        except requests.RequestException as e:
            console.print(f"[red][!] Request failed: {e}[/red]")
            return None
