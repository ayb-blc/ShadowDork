import json
import os
import sys
from rich import print

def load_dorks(data_folder="data"):
    """
    MODULAR STRUCTURE:
    Reads all .json files (sqli.json, git.json, etc.) in the 'data' folder.
    Uses the file name as the category name and merges them into a single dictionary.
    """
    # 1. Check if there is a folder
    if not os.path.exists(data_folder):
        print(f"[bold red][!] ERROR: '{data_folder}' folder not found![/bold red]")
        print(f"[yellow]    Please create a 'data' folder.[/yellow]")
        sys.exit(1)

    combined_dorks = {}
    
    # 2. Find.json files in folder
    files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
    
    if not files:
        print(f"[bold red][!] ERROR: '{data_folder}' folder is empty![/bold red]")
        print(f"[yellow]    Please add category files (git.json, sqli.json etc.) to it.[/yellow]")
        sys.exit(1)

    # print(f"[dim] Scanning the database... ({len(files)} file)[/dim]")

    # 3. Read and merge each file individually
    for filename in files:
        file_path = os.path.join(data_folder, filename)
        
        category_name = filename.replace(".json", "")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                dork_list = json.load(f)
                
                if isinstance(dork_list, list):
                    combined_dorks[category_name] = dork_list
                else:
                    print(f"[yellow][!] Warning: '{filename}' file format is incorrect (List [] expected). Skipped.[/yellow]")

        except json.JSONDecodeError:
            print(f"[bold red][!] ERROR: '{filename}' is corrupted JSON format![/bold red]")
        except Exception as e:
            print(f"[red][!] An error occurred while loading '{filename}': {e}[/red]")

    return combined_dorks