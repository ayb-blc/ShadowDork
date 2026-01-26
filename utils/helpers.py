import webbrowser
import time
import sys
import shutil

# For colored warnings (if Rich is available, we use it, otherwise it is plain print)
def log(msg):
    print(f"[*] {msg}")

def get_browser_controller(browser_name):
    """
    Checks if the desired browser is registered in the system
    and returns the controller object.
    """
    
    # Common browser paths for Linux/Mac
    # If you are using Windows, you need to add.exe paths.
    browser_paths = {
        "chrome": ["google-chrome", "chrome", "google-chrome-stable"],
        "firefox": ["firefox"],
        "brave": ["brave-browser", "brave"],
        "tor": ["tor-browser", "tor-browser-en", "start-tor-browser"],
        "chromium": ["chromium", "chromium-browser"]
    }

    if browser_name == "default":
        return webbrowser.get() # The default of the system is

    # 1. Is the browser already registered in Python? (Firefox is usually registered)
    try:
        return webbrowser.get(browser_name)
    except webbrowser.Error:
        pass # If it is not registered, we will try the ways

    # 2. If not, see if there is a PATH in the system path
    if browser_name in browser_paths:
        possible_cmds = browser_paths[browser_name]
        for cmd in possible_cmds:
            path = shutil.which(cmd) # The 'which' command in Linux
            if path:
                log(f"{browser_name} found: {path}")
                # Register browser
                webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(path))
                return webbrowser.get(browser_name)
    
    log(f"[!] ERROR: '{browser_name}' browser not found!")
    log(f"    Make sure the browser is installed or added to PATH.")
    sys.exit(1)

def open_tabs(url_list, browser_name="default", delay=1.5):
    """
    Opens links in the specified browser.
    """
    controller = get_browser_controller(browser_name)
    
    log(f"Browser: {browser_name.upper()} ({len(url_list)} tabs)")
    
    for url in url_list:
        try:
            controller.open_new_tab(url)
            time.sleep(delay)
        except KeyboardInterrupt:
            print("\n[!] Stopped.")
            sys.exit(0)

def parse_indexes(index_str):
    """
    Converts the string input (e.g: "1-3,5,10") 
    to a list of numbers: [1, 2, 3, 5, 10]
    """
    selected_indexes = set()
    try:
        parts = index_str.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                # If range is specified (e.g: 1-5)
                start, end = map(int, part.split('-'))
                # range does not include the last number, so we add +1
                selected_indexes.update(range(start, end + 1))
            else:
                # If single number (e.g: 5)
                selected_indexes.add(int(part))
        return sorted(list(selected_indexes))
    except ValueError:
        return []