import os

class PayloadManager:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'payloads')
        
    def get_payload(self, name):
        """
        Returns (filename, content, content_type) for a named payload.
        Reads from the data directory.
        """
        payload_map = {
            "test-txt": ("test.txt", "harmless_test_files/test.txt", "text/plain"), # We'll create this one too or just use string
            "php-webshell": ("shell.php", "php/simple_shell.php", "application/x-php"),
            "asp-webshell": ("shell.aspx", "asp/simple_shell.aspx", "application/x-asp"),
            "jsp-webshell": ("shell.jsp", "jsp/simple_shell.jsp", "application/x-jsp"),
            "php-image-polyglot": ("logo.gif", "polyglots/gif_php.gif", "image/gif"),
            "svg-xss": ("xss.svg", "harmless_test_files/xss.svg", "image/svg+xml"),
            "htaccess-php": (".htaccess", "php/malicious.htaccess", "application/octet-stream"),
        }

        if name in payload_map:
            fname, rel_path, mime = payload_map[name]
            
            # Special case for simple test text if file doesn't exist yet
            if name == "test-txt":
                 return fname, b"CerberusFUEF_Test_File", mime

            full_path = os.path.join(self.base_path, rel_path)
            try:
                with open(full_path, 'rb') as f:
                    content = f.read()
                return fname, content, mime
            except FileNotFoundError:
                # Fallback if file missing
                return fname, b"ERROR_PAYLOAD_MISSING", mime
        else:
            return "unknown.txt", b"test", "text/plain"

    def list_payloads(self):
        return ["test-txt", "php-webshell", "asp-webshell", "jsp-webshell", "php-image-polyglot", "svg-xss", "htaccess-php"]
