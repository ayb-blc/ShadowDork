# 🕵️‍♂️ ShadowDork

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-grey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable-orange?style=for-the-badge)

**The Invisible Hand of OSINT.** *Advanced, Stealthy, and Modular Google Hacking Assistant.*

</div>

---

## Overview

**ShadowDork** is a next-generation command-line tool designed for **Bug Bounty Hunters**, **Pentesters**, and **Security Researchers**. 

Unlike traditional dorking tools that aggressively query Google and get blocked by CAPTCHAs instantly, ShadowDork utilizes a **Hybrid Search Architecture**. It leverages **DuckDuckGo's search infrastructure** as a proxy to filter and verify active dorks without directly triggering Google's bot detection systems. 

It transforms the tedious process of Google Hacking into a streamlined, automated, and safe workflow.

## Key Features

* **Anti-Ban Architecture (Stealth Mode):** Uses DuckDuckGo as a "Oracle" to verify if a dork returns results before you ever open Google. This minimizes interaction with Google servers, reducing the risk of IP bans and CAPTCHAs by **99%**.
* **Smart Verification Engine:** The `-x` (check) flag doesn't just ping the URL. It performs **Client-Side Validation** to ensure the target domain matches and eliminates false positives caused by search engine fuzziness.
* **Modular Data Structure:** No more massive, unmanageable JSON files. Dorks are split into categorized files (`git.json`, `sqli.json`, `exposed_services.json`), making it easy to maintain and contribute.
* **Precision Targeting:** Includes a "Grep" feature (`-g`) to run specific payloads (e.g., `-g 1-5,10`) instead of scanning the entire category.
* **Preview Mode:** Inspect payloads with IDs before running them using the `-P` flag.
* **Rich CLI Interface:** Beautiful, readable, and interactive terminal output powered by the `rich` library.

## Installation

### Prerequisites
* Python 3.8 or higher
* pip (Python Package Manager)

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/ayb-blc/ShadowDork.git](https://github.com/ayb-blc/ShadowDork.git)
    cd ShadowDork
    ```

2.  **Run the Installer**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    *This script will set up a virtual environment, install requirements, and create a `./shadowdork` shortcut.*

## Usage

ShadowDork is designed to be intuitive.

### 1. Basic Scan
Generate search links for a specific category and target.
```bash
./shadowdork -t uber.com -c git -o
```


### 2. Stealth Live Check (Recommended)

Verify which dorks actually return results before opening them in the browser.

```bash
./shadowdork -t uber.com -c files_sensitive -x -o -b firefox
```

### 3. Preview & Select Specific Payloads
```bash
./shadowdork -c login -P
```

Then, run only the selected IDs (e.g., ID 1, 2, and 5):
```bash
./shadowdork -t uber.com -c login -g 1,2,5 -x -o -b brave
```

### 4. List All Categories
```bash
./shadowdork -l
```

## Arguments

Argument,Long Flag,Description
-t,--target,"Target domain (e.g., example.com)."
-c,--category,"Dork category (e.g., git, sqli, logs)."
-x,--check,Live Check Mode. Verifies results via DDG to prevent empty tabs.
-o,--open,Automatically opens valid links in your default browser.
-g,--grep,"Select specific Dork IDs to run (e.g., 1-5 or 1,3,9)."
-P,--preview,Lists payloads in a category with IDs without running them.
-l,--list,Lists all available categories in the database.
-e,--engine,Search engine logic (Default: ddg).
-b,--browser,"Specify browser (chrome, firefox, brave, default)."

## Data Structure (Modularity)

ShadowDork uses a modular JSON system located in the data/ directory. Each file represents a category.

data/
├── git.json             # Git exposure dorks
├── sqli.json            # SQL Injection patterns
├── files_sensitive.json # .env, .conf, .log files
├── cloud_storage.json   # AWS S3, Azure Blob leaks
└── ...

Want to add new dorks? Simply create a new .json file in the data/ folder (e.g., wordpress.json). The tool will automatically detect and load it on the next run. No code changes required!

## ⚠️ Legal Disclaimer

ShadowDork is created for educational purposes and authorized security testing (Pentesting/Bug Bounty) only.

    Do not use this tool on domains you do not own or do not have explicit permission to audit.

    The developer assumes no responsibility for any misuse or damage caused by this program.

    Google Dorking is a passive reconnaissance technique, but automated queries may violate some Terms of Service. Use responsibly.


## 🤝 Contributing

Contributions are welcome! If you have a new list of dorks or a feature idea:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/AmazingFeature).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

_______________________________________________________________________________________________________________________________

<div align="center">

Made with ❤️ by [Ayberk Balcı](https://github.com/ayb-blc)

</div>
