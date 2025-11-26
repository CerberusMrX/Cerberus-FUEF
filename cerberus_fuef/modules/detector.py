from bs4 import BeautifulSoup
from urllib.parse import urljoin
from rich.console import Console

console = Console()

class Detector:
    def __init__(self, http_client):
        self.client = http_client

    def scan_url(self, url):
        """
        Scans a single URL for file upload forms.
        """
        console.print(f"[blue][*] Scanning {url} for upload forms...[/blue]")
        response = self.client.get(url)
        
        if not response:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        candidates = []

        for form in forms:
            # Check if form has input type="file"
            file_inputs = form.find_all('input', {'type': 'file'})
            
            if file_inputs:
                action = form.get('action')
                method = form.get('method', 'GET').upper()
                
                # Resolve relative action URL
                if action:
                    action_url = urljoin(url, action)
                else:
                    action_url = url
                
                file_fields = [fi.get('name') for fi in file_inputs if fi.get('name')]
                
                # Get other inputs
                other_inputs = {}
                for inp in form.find_all('input'):
                    if inp.get('type') != 'file' and inp.get('name'):
                        other_inputs[inp.get('name')] = inp.get('value', '')

                candidate = {
                    "url": action_url,
                    "method": method,
                    "file_fields": file_fields,
                    "other_fields": other_inputs
                }
                candidates.append(candidate)
                
                console.print(f"[green][+] Found upload form![/green]")
                console.print(f"    Action: {action_url}")
                console.print(f"    Method: {method}")
                console.print(f"    File Fields: {file_fields}")
                console.print(f"    Other Fields: {other_inputs}")

        if not candidates:
            console.print("[yellow][-] No upload forms found on this page.[/yellow]")
            
        return candidates
