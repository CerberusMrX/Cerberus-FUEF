import json
import os
from rich.console import Console

console = Console()

class Reporter:
    def __init__(self):
        pass

    def generate_json(self, data, filename="report.json"):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            console.print(f"[green][+] JSON report saved to {filename}[/green]")
        except Exception as e:
            console.print(f"[red][!] Failed to save JSON report: {e}[/red]")

    def generate_html(self, data, filename="report.html"):
        # Basic HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cerberus FUEF Report</title>
            <style>
                body {{ font-family: sans-serif; margin: 40px; background: #f4f4f4; }}
                .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                h1 {{ color: #d32f2f; }}
                h2 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                .success {{ color: green; font-weight: bold; }}
                .failure {{ color: red; }}
                pre {{ background: #eee; padding: 10px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Cerberus FUEF Scan Report</h1>
                <p><strong>Target:</strong> {data.get('target', 'Unknown')}</p>
                
                <h2>Fingerprint</h2>
                <pre>{json.dumps(data.get('fingerprint', {}), indent=2)}</pre>
                
                <h2>Attack Results</h2>
                <ul>
        """
        
        for result in data.get('attacks', []):
            status_class = "success" if result.get('success') else "failure"
            html_content += f"""
                <li class="{status_class}">
                    <strong>{result.get('strategy')}</strong>: {result.get('filename')} 
                    (Status: {result.get('status_code')})
                    <br>
                    <code style="display:block; margin-top:5px; font-size: 0.8em; color: #555;">{result.get('curl_command', '')}</code>
                </li>
            """
            
        html_content += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        try:
            with open(filename, 'w') as f:
                f.write(html_content)
            console.print(f"[green][+] HTML report saved to {filename}[/green]")
        except Exception as e:
            console.print(f"[red][!] Failed to save HTML report: {e}[/red]")
