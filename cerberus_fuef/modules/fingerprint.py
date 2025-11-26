from rich.console import Console
from cerberus_fuef.core.target_profile import TargetFingerprint

console = Console()

import concurrent.futures

class Fingerprinter:
    def __init__(self, http_client):
        self.client = http_client
        self.extensions = [".php", ".php5", ".phtml", ".asp", ".aspx", ".jsp", ".html", ".txt", ".jpg", ".png", ".gif", ".svg", ".xml"]
        self.mime_types = ["application/x-php", "image/jpeg", "image/png", "text/plain", "application/octet-stream", "image/svg+xml"]

    def _test_extension(self, endpoint, field, ext, method):
        filename = f"test{ext}"
        content = b"CerberusFUEF_Test"
        files = {field: (filename, content, "application/octet-stream")}
        
        try:
            if method == "POST":
                resp = self.client.post(endpoint, files=files)
            else:
                resp = None
            return ext, resp
        except:
            return ext, None

    def fingerprint(self, endpoint, field, method="POST"):
        console.print(f"[blue][*] Starting MAX LEVEL fingerprinting on {endpoint}...[/blue]")
        
        allowed_exts = []
        rejected_exts = []
        
        # 1. Test Extensions with Threading
        console.print("[dim][*] Testing extensions (Parallel)...[/dim]")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._test_extension, endpoint, field, ext, method): ext for ext in self.extensions}
            
            for future in concurrent.futures.as_completed(futures):
                ext = futures[future]
                try:
                    _, resp = future.result()
                    if resp:
                        if 200 <= resp.status_code < 300:
                            console.print(f"    [green][+] Allowed: {ext} ({resp.status_code})[/green]")
                            allowed_exts.append(ext)
                        elif resp.status_code == 403 or resp.status_code == 401:
                            console.print(f"    [red][-] Forbidden: {ext} ({resp.status_code})[/red]")
                            rejected_exts.append(ext)
                        elif resp.status_code == 413:
                            console.print(f"    [yellow][!] Too Large: {ext} ({resp.status_code})[/yellow]")
                        elif resp.status_code == 500:
                            console.print(f"    [yellow][!] Server Error: {ext} ({resp.status_code})[/yellow]")
                            rejected_exts.append(ext)
                        else:
                            console.print(f"    [dim][?] Unknown: {ext} ({resp.status_code})[/dim]")
                            rejected_exts.append(ext)
                except Exception as e:
                    console.print(f"    [red][!] Error testing {ext}: {e}[/red]")
        
        # Create result object
        fp = TargetFingerprint(
            allowed_extensions=allowed_exts,
            rejected_extensions=rejected_exts
        )
        
        console.print(f"[bold green][+] Fingerprinting complete.[/bold green]")
        console.print(f"    Allowed Extensions: {allowed_exts}")
        
        return fp
