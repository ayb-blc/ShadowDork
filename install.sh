#!/bin/bash

# Colors
RED='\033[1;31m'   # Bold Red
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
DIM='\033[2m'      # Dim (Sönük)
NC='\033[0m'       # No Color

# Banner
echo -e "${RED}"
cat << "EOF"
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ 
    ██████╗  ██████╗ ██████╗ ██╗  ██╗              
    ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝              
    ██║  ██║██║   ██║██████╔╝█████╔╝               
    ██║  ██║██║   ██║██╔══██╗██╔═██╗               
    ██████╔╝╚██████╔╝██║  ██║██║  ██╗              
    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝              
EOF
echo -e "${NC}"
echo -e "      ${DIM}>> The Invisible Hand of OSINT <<${NC}\n"

echo -e "${BLUE}[+] ShadowDork Installation Wizard Starting...${NC}"

# 1. Python3 Check
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] ERROR: Python3 is not installed! Please install Python3 first.${NC}"
    exit 1
fi

# 2. Sanal Ortam (venv) Check and Installation
if [ -d "venv" ]; then
    echo -e "${YELLOW}[!] Virtual environment already exists. Updating...${NC}"
else
    echo -e "${GREEN}[+] Virtual environment (venv) is being created...${NC}"
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[!] Virtual environment could not be created.${NC}"
        echo -e "${YELLOW}[i] Please run the following command and try again:${NC}"
        echo -e "    sudo apt install python3-venv -y"
        exit 1
    fi
fi

# 3. Install Dependencies
echo -e "${GREEN}[+] Installing required packages...${NC}"
./venv/bin/pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}[!] Package installation failed!${NC}"
    exit 1
fi

# 4. Create Run Shortcut
echo -e "#!/bin/bash\n./venv/bin/python3 main.py \"\$@\"" > shadowdork
chmod +x shadowdork

echo -e "${GREEN}
=========================================
[✓] Installation Completed!
=========================================${NC}"
echo -e "${YELLOW}[?] To run the tool, just type:${NC}"
echo -e "${RED}    ./shadowdork -l${NC}"
echo ""