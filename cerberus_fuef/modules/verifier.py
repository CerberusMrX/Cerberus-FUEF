from rich.console import Console
from urllib.parse import urljoin

console = Console()

import os
import re
import json

class Verifier:
    def __init__(self, http_client):
        self.client = http_client
        # Load wordlist
        self.wordlist_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordlists', 'common_paths.txt')
        self.common_paths = []
        if os.path.exists(self.wordlist_path):
            with open(self.wordlist_path, 'r') as f:
                self.common_paths = [line.strip() for line in f if line.strip()]
        else:
            self.common_paths = ["uploads/", "images/", "files/"]

    def extract_paths_from_response(self, response_text):
        """
        Extracts potential file paths from JSON or HTML response.
        """
        candidates = []
        
        # 1. Try JSON parsing
        try:
            data = json.loads(response_text)
            # Recursively search for string values that look like paths or urls
            def search_json(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        search_json(v)
                elif isinstance(obj, list):
                    for item in obj:
                        search_json(item)
                elif isinstance(obj, str):
                    if '/' in obj or '.' in obj:
                        candidates.append(obj)
            search_json(data)
        except json.JSONDecodeError:
            pass

        # 2. Regex for common patterns in HTML
        # Look for src="..." or href="..." or just strings ending in extensions
        # Simple regex to find strings that look like the uploaded filename
        # This is heuristic.
        pass 
        
        return candidates

    def verify_upload(self, base_url, filename, content_fingerprint=None, upload_response=None):
        """
        Attempts to find the uploaded file.
        """
        console.print(f"[blue][*] Verifying upload for {filename}...[/blue]")
        
        potential_urls = []
        base_dir = base_url.rsplit('/', 1)[0] + '/'
        
        # 1. Check if response leaked the path
        if upload_response and upload_response.text:
            leaked_paths = self.extract_paths_from_response(upload_response.text)
            for path in leaked_paths:
                # Handle relative vs absolute
                if path.startswith('http'):
                    potential_urls.append(path)
                elif path.startswith('/'):
                    # Root relative
                    root = '/'.join(base_url.split('/')[:3]) # http://site.com
                    potential_urls.append(root + path)
                else:
                    potential_urls.append(urljoin(base_dir, path))
                    
        # 2. Guess paths from wordlist
        potential_urls.append(urljoin(base_dir, filename))
        for path in self.common_paths:
            potential_urls.append(urljoin(base_dir, path + filename))
            
        # Deduplicate
        potential_urls = list(set(potential_urls))
            
        found_url = None
        
        for url in potential_urls:
            # console.print(f"[dim]    Checking {url}...[/dim]") # Too noisy if list is long
            try:
                resp = self.client.get(url)
                
                if resp and resp.status_code == 200:
                    # Check content if fingerprint provided
                    if content_fingerprint:
                        if content_fingerprint in resp.content:
                            console.print(f"[bold green][!] FILE FOUND AND VERIFIED: {url}[/bold green]")
                            found_url = url
                            break
                    else:
                        console.print(f"[bold green][!] File found (status 200): {url}[/bold green]")
                        found_url = url
                        break
            except:
                pass
                    
        if not found_url:
            console.print("[yellow][-] Could not locate uploaded file.[/yellow]")
            
        return found_url
