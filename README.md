# Cerberus FUEF 🐕‍🦺🔥

<img width="1646" height="605" alt="cbsfufe" src="https://github.com/user-attachments/assets/37cb7701-a7ba-4984-bce7-c494407b1052" />

### Cerberus File Upload Exploitation Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Type](https://img.shields.io/badge/Type-Offensive%20Security-red)

> **"Unleash the hound on insecure file uploads."**

**Cerberus FUEF** is a professional-grade offensive security framework designed to assist penetration testers and red teamers in **discovering, fingerprinting, and exploiting** insecure file upload functionalities in web applications.

It automates the tedious process of testing file uploads, systematically attempting advanced bypass techniques, and verifying successful execution—all while generating professional reports with reproducible steps.

---

## ⚠️ Legal Disclaimer

> [!CAUTION]
> **FOR AUTHORIZED SECURITY TESTING ONLY.**
>
> This tool is designed for security professionals and researchers. You must have explicit, written permission from the target system's owner before using this tool. The author (**Sudeepa Wanigarathna**) accepts no responsibility for any misuse, damage, or illegal activities caused by this tool. Use responsibly and ethically.

---

## ✨ Key Features

*   **🕵️ Automatic Detection**: Crawl URLs to discover hidden file upload forms and extract parameters.
*   **🔍 Intelligent Fingerprinting**: Probe endpoints to identify allowed extensions (e.g., `.php`, `.jpg`) and MIME types.
*   **🔓 Advanced Bypass Engine**:
    *   **Null Byte Injection** (`shell.php%00.jpg`)
    *   **Double Extensions** (`shell.php.jpg`)
    *   **MIME Type Spoofing** (`image/jpeg` headers)
    *   **Path Traversal** (`../../shell.php`)
    *   **Case Sensitivity** (`shell.PhP`)
*   **💣 Payload Library**:
    *   **Webshells**: PHP, ASPX, JSP.
    *   **Polyglots**: Valid GIF images containing hidden PHP code.
    *   **XSS**: SVG payloads for Stored XSS.
    *   **Apache Override**: Malicious `.htaccess` files.
*   **✅ Auto-Verification**: Automatically checks if uploaded files are accessible and executable on the server.
*   **📝 Professional Reporting**: Generates HTML reports containing exact `curl` commands to manually reproduce every successful exploit.
*   **⚡ High Performance**: Multi-threaded architecture for rapid scanning and exploitation.

---

## 🚀 Installation

### Prerequisites
*   **Python 3.10+**
*   **Kali Linux** (Recommended), macOS, or Windows.

### Quick Install

```bash
# 1. Clone the repository
git clone https://github.com/CerberusMrX/cerberus-fuef.git
cd cerberus-fuef

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python3 -m cerberus_fuef.main --help
```

> **Note for Kali Linux Users**: If you encounter an "externally managed environment" error, use a virtual environment:
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> ```

---

## 📖 Usage Guide

Cerberus FUEF is a CLI tool. The general syntax is:

```bash
python3 -m cerberus_fuef.main [COMMAND] [OPTIONS]
```

### 1. Detect Upload Forms
Scan a URL to find upload endpoints.

```bash
python3 -m cerberus_fuef.main detect --url https://target.com/contact
```

### 2. Fingerprint Endpoint
Send harmless test files to see what the server accepts.

```bash
python3 -m cerberus_fuef.main fingerprint \
    --endpoint https://target.com/upload.php \
    --field file
```

### 3. Attack (The Fun Part)
Attempt to upload a payload using bypass techniques.

**Example: Max Level Attack**
This runs all bypass strategies (Null Byte, Double Ext, etc.) and verifies the result.

```bash
python3 -m cerberus_fuef.main attack \
    --endpoint https://target.com/upload.php \
    --field file \
    --payload php-webshell \
    --use-bypass-strategy all \
    --verify \
    --output report.html
```

**Example: Polyglot Upload**
Bypass image filters by uploading a valid GIF with hidden PHP.

```bash
python3 -m cerberus_fuef.main attack \
    --endpoint https://target.com/gallery/upload \
    --field image \
    --payload php-image-polyglot \
    --verify
```

### Global Options
*   `--proxy http://127.0.0.1:8080`: Route traffic through Burp Suite/Zap.
*   `--cookie "PHPSESSID=..."`: Authenticated scanning.
*   `--verbose`: See every request and response.

---

## 📦 Payload Types

| Payload | Description |
| :--- | :--- |
| `test-txt` | Harmless text file for connectivity testing. |
| `php-webshell` | Simple PHP command shell. |
| `asp-webshell` | ASPX command shell. |
| `jsp-webshell` | JSP command shell. |
| `php-image-polyglot` | Valid GIF header + PHP code (Bypasses `getimagesize`). |
| `svg-xss` | SVG image with embedded JavaScript (Stored XSS). |
| `htaccess-php` | Malicious `.htaccess` to enable PHP in upload dirs. |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Author**: Sudeepa Wanigarathna
