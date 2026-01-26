import time
import random
import urllib.parse
from rich import print
from rich.progress import track

# DDGS import
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

def is_valid_broad(dork_payload, result):
    """
    Expanded control:
    It doesn't only look at the URL. It also searches in the title (title) and description (body).
    So it catches results even if they are not written in the URL but in the description.
    """
    dork_payload = dork_payload.lower()
    
    # DDG result data (all lowercase)
    res_url = urllib.parse.unquote(result.get('href', '')).lower()
    res_title = result.get('title', '').lower()
    res_body = result.get('body', '').lower()
    
    # Combine all content (URL + Title + Description)
    full_content = f"{res_url} {res_title} {res_body}"

    # --- 1. DOMAIN CONTROL (Always mandatory) ---
    if "site:" in dork_payload:
        parts = dork_payload.split(" ")
        for part in parts:
            if part.startswith("site:"):
                target_domain = part.replace("site:", "").strip('"')
                if target_domain not in res_url:
                    return False, f"Invalid Domain: {res_url}"

    # --- 2. KEYWORD CONTROL ---
    # Remove critical keywords from the dork (site: excluded)
    keywords = []
    parts = dork_payload.split(" ")
    for part in parts:
        if part.startswith("site:"): continue
        
        # Remove prefix like inurl, intext, ext, etc. and get the clean word
        clean_word = part.replace("inurl:", "").replace("intext:", "").replace("intitle:", "").replace("ext:", "").strip('"')
        
        # If the word contains "/", split it (e.g: .git/config -> .git and config)
        if "/" in clean_word:
            keywords.extend(clean_word.split("/"))
        else:
            keywords.append(clean_word)

    # If there are no keywords (only site:uber.com), accept it
    if not keywords:
        return True, "Domain Match"

    # Is at least one of the keywords in any part of the content?
    for kw in keywords:
        if kw in full_content:
            # Return the keyword that was found (Debug for)
            return True, f"Found Keyword: '{kw}'"

    return False, f"Keyword Not Found ({keywords})"


def filter_active_dorks(dork_list_with_links, delay_range=(0.5, 1.5)):
    active_links = []
    
    print(f"\n[bold yellow]$ DEEP ANALYSIS MODE (-x) STARTED...[/bold yellow]")
    print(f"[dim]URL, Title and Description are being scanned... (Debug Open)[/dim]\n")

    try:
        with DDGS() as ddgs:
            for item in track(dork_list_with_links, description="[cyan]Scanning...[/cyan]"):
                
                payload = item['payload']
                google_link = item['link']
                
                try:
                    # DDG Araması
                    results = list(ddgs.text(
                        payload, 
                        region='wt-wt', 
                        safesearch='off', 
                        backend='html', 
                        max_results=1 
                    ))
                    
                    if len(results) > 0:
                        first_result = results[0]
                        found_url = first_result.get('href', 'N/A')
                        
                        # Expanded Validation
                        is_valid, msg = is_valid_broad(payload, first_result)
                        
                        if is_valid:
                            print(f"[bold green]✓ FOUND:[/bold green] {payload}")
                            # print(f"  └─ [dim]{msg} -> {found_url}[/dim]") # Open it if you want to see the details.
                            active_links.append(google_link)
                        else:
                            # DEBUG
                            print(f"[yellow]⚠ Elendi:[/yellow] {payload}")
                            print(f"  └─ [red]Reason: {msg}[/red]")
                            print(f"  └─ [dim]Link: {found_url}[/dim]")
                    else:
                        print(f"[dim]x Empty:[/dim] {payload}")
                        
                except Exception as e:
                    if "Ratelimit" in str(e):
                        print(f"[bold red]* Rate Limit! 3sn pause...[/bold red]")
                        time.sleep(3)
                    else:
                        print(f"[red]! Error:[/red] {payload}")

                time.sleep(random.uniform(*delay_range))

    except Exception as session_error:
        print(f"[bold red][!] Critical Error:[/bold red] {session_error}")
        return active_links

    return active_links