import argparse
import sys
from rich import print

from core.dork_loader import load_dorks
from core.generator import generate_query, create_search_url 
from ui.console import print_banner, list_categories, preview_payloads, show_results_table
from utils.helpers import open_tabs, parse_indexes
from utils.checker import filter_active_dorks

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="LazyDork v1.1", add_help=False)
    
    
    req_group = parser.add_argument_group('Temel Ayarlar')
    req_group.add_argument("-t", "--target", help="Target Domain (e.g: uber.com)")
    req_group.add_argument("-c", "--category", help="Dork Category (e.g: git, login)")
    
    act_group = parser.add_argument_group('Actions')
    act_group.add_argument("-l", "--list", action="store_true", help="List categories and exit")
    act_group.add_argument("-P", "--preview", action="store_true", help="List payloads from the selected category (to see IDs)")
    act_group.add_argument("-g", "--grep", help="Run only specific IDs (e.g: 1-5 or 1,3,10)")
    
    browser_group = parser.add_argument_group('Browser & Control')
    browser_group.add_argument("-o", "--open", action="store_true", help="Open links in browser")
    browser_group.add_argument("-x", "--check", action="store_true", help="Live check (Only open active links)")
    browser_group.add_argument("-b", "--browser", default="default", choices=["chrome", "firefox", "brave", "tor", "default"])
    browser_group.add_argument("-e", "--engine", default="ddg", 
                        help="Search Engine (Default: DDG)", 
                        choices=["google", "ddg", "bing"])
    
    parser.add_argument("-h", "--help", action="help", help="Show help message")

    args = parser.parse_args()
    
    # 1. Load Database
    all_dorks_data = load_dorks()

    # --- STATUS 1: LISTING (-l) ---
    if args.list:
        list_categories(all_dorks_data)
        sys.exit(0)


    if not args.category:
        print("[bold red][!] ERROR: You must select a category (-c)![/bold red]")
        print("[yellow]    To see categories: python main.py -l[/yellow]")
        sys.exit(1)

    if args.category not in all_dorks_data:
        print(f"[bold red][!] ERROR: '{args.category}' category not found![/bold red]")
        sys.exit(1)

    selected_raw_dorks = all_dorks_data[args.category]

    # --- STATUS 2: PREVIEW (-P) ---
    if args.preview:
        preview_payloads(selected_raw_dorks, args.category)
        sys.exit(0)

    # --- STATUS 3: PROCESSING ---
    if not args.target:
        print("[bold red][!] ERROR: Target domain (-t) not specified![/bold red]")
        sys.exit(1)

    # --- FILTER (-g) ---
    final_dork_list = []
    
    if args.grep:
        desired_indexes = parse_indexes(args.grep)
        print(f"[bold cyan] Filtre Uygulanıyor:[/bold cyan] Sadece {desired_indexes} ID'li dorklar seçildi.")
        
        for i in desired_indexes:
            if 1 <= i <= len(selected_raw_dorks):
                dork_item = selected_raw_dorks[i-1]
                dork_item['original_id'] = i 
                final_dork_list.append(dork_item)
            else:
                print(f"[dim][!] ID {i} listede yok, atlanıyor.[/dim]")
                
        if not final_dork_list:
            print("[bold red][!] Selected IDs not found![/bold red]")
            sys.exit(1)
    else:
        final_dork_list = selected_raw_dorks

    # --- LINK GENERATION ---
    processed_list = []
    
    for item in final_dork_list:
        final_query = generate_query(item['payload'], args.target)
        search_link = create_search_url(final_query, engine=args.engine)
        
        processed_list.append({
            "original_id": item.get('original_id', final_dork_list.index(item)+1),
            "desc": item['desc'],
            "payload": final_query, 
            "link": search_link
        })

    # --- LIVE CHECK (-x) ---
    final_urls_to_open = []

    if args.check:
        valid_links = filter_active_dorks(processed_list)
        final_urls_to_open = valid_links
    else:
        final_urls_to_open = [item['link'] for item in processed_list]
        show_results_table(processed_list)

    # --- OPEN IN BROWSER (-o) ---
    if args.open:
        if len(final_urls_to_open) == 0:
            print("[red][!] No links to open.[/red]")
            sys.exit(0)

        if len(final_urls_to_open) > 10:
            ans = input(f"\n[?] {len(final_urls_to_open)} tabs will be opened. Continue? (y/n): ")
            if ans.lower() != 'y': sys.exit(0)
        
        open_tabs(final_urls_to_open, browser_name=args.browser)

if __name__ == "__main__":
    main()