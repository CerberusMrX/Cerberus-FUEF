import argparse
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def print_banner():
    banner = """
   ______          _                      
  / ____/___  ____| |__   ___ _ __ _   _ ___ 
 / /   / _ \/ ___| '_ \ / _ \ '__| | | / __|
/ /___|  __/ |   | |_) |  __/ |  | |_| \__ \\
\____/ \___|_|   |_.__/ \___|_|   \__,_|___/
    FUEF - File Upload Exploitation Framework
    """
    console.print(f"[bold red]{banner}[/bold red]")
    console.print("[bold white]Cerberus FUEF – Cerberus File Upload Exploitation Framework[/bold white]")
    console.print("[bold white]Author: Sudeepa Wanigarathna[/bold white]")
    console.print("[bold yellow]For authorized security testing and research only.[/bold yellow]\n")

from cerberus_fuef.core.http_client import HTTPClient
from cerberus_fuef.modules.detector import Detector
from cerberus_fuef.modules.fingerprint import Fingerprinter
from cerberus_fuef.modules.payloads import PayloadManager
from cerberus_fuef.modules.bypass_strategies import BypassEngine
from cerberus_fuef.modules.verifier import Verifier
from cerberus_fuef.core.reporter import Reporter

def get_client(args):
    return HTTPClient(
        proxy=args.proxy,
        cookies=args.cookie,
        headers=args.header,
        timeout=args.timeout,
        verbose=args.verbose
    )

def handle_detect(args):
    console.print(f"[bold blue][*] Mode:[/bold blue] Detect")
    console.print(f"[bold blue][*] Target URL:[/bold blue] {args.url}")
    
    client = get_client(args)
    detector = Detector(client)
    detector.scan_url(args.url)

def handle_fingerprint(args):
    console.print(f"[bold blue][*] Mode:[/bold blue] Fingerprint")
    console.print(f"[bold blue][*] Endpoint:[/bold blue] {args.endpoint}")
    
    client = get_client(args)
    fp = Fingerprinter(client)
    fp.fingerprint(args.endpoint, args.field, args.method)

def handle_attack(args):
    console.print(f"[bold blue][*] Mode:[/bold blue] Attack")
    console.print(f"[bold blue][*] Endpoint:[/bold blue] {args.endpoint}")
    console.print(f"[bold blue][*] Payload:[/bold blue] {args.payload}")
    
    client = get_client(args)
    pm = PayloadManager()
    
    filename, content, mime = pm.get_payload(args.payload)
    console.print(f"[dim][*] Loaded payload: {filename} ({len(content)} bytes)[/dim]")
    
    engine = BypassEngine(client)
    results = engine.run_attack(args.endpoint, args.field, args.payload, content, filename, args.use_bypass_strategy)
    
    if args.verify:
        verifier = Verifier(client)
        for res in results:
            if res['success']:
                verifier.verify_upload(
                    args.endpoint, 
                    res['filename'], 
                    content_fingerprint=content if len(content) < 50 else None,
                    upload_response=res.get('response')
                )

    if args.output:
        reporter = Reporter()
        report_data = {
            "target": args.endpoint,
            "attacks": results
        }
        if args.output.endswith('.json'):
            reporter.generate_json(report_data, args.output)
        else:
            reporter.generate_html(report_data, args.output)

def handle_full(args):
    console.print(f"[bold blue][*] Mode:[/bold blue] Full Scan")
    console.print(f"[bold blue][*] URL:[/bold blue] {args.url}")
    console.print("[yellow][!] Full scan logic combines detect -> fingerprint -> attack. (To be implemented in next iteration)[/yellow]")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Cerberus FUEF - File Upload Exploitation Framework")
    
    # Global arguments
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--cookie", help="Cookies (e.g., 'PHPSESSID=...; token=...')")
    parser.add_argument("--header", action="append", help="Custom headers (e.g., 'X-Custom: value')")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--output", help="Output report file")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Detect Command
    parser_detect = subparsers.add_parser("detect", help="Detect file upload forms")
    parser_detect.add_argument("--url", required=True, help="Target URL to crawl")
    
    # Fingerprint Command
    parser_fingerprint = subparsers.add_parser("fingerprint", help="Fingerprint upload behavior")
    parser_fingerprint.add_argument("--endpoint", required=True, help="Upload endpoint URL")
    parser_fingerprint.add_argument("--field", required=True, help="File input field name")
    parser_fingerprint.add_argument("--method", default="POST", help="HTTP method (default: POST)")

    # Attack Command
    parser_attack = subparsers.add_parser("attack", help="Attempt exploitation")
    parser_attack.add_argument("--endpoint", required=True, help="Upload endpoint URL")
    parser_attack.add_argument("--field", required=True, help="File input field name")
    parser_attack.add_argument("--payload", required=True, help="Payload type (e.g., php-webshell)")
    parser_attack.add_argument("--use-bypass-strategy", default="all", help="Bypass strategy to use")
    parser_attack.add_argument("--verify", action="store_true", help="Verify upload success")

    # Full Command
    parser_full = subparsers.add_parser("full", help="Full automated scan")
    parser_full.add_argument("--url", required=True, help="Target URL")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "detect":
        handle_detect(args)
    elif args.command == "fingerprint":
        handle_fingerprint(args)
    elif args.command == "attack":
        handle_attack(args)
    elif args.command == "full":
        handle_full(args)

if __name__ == "__main__":
    main()
