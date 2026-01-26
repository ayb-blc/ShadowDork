from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()

def print_banner():
    banner = r"""
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
    """
    console.print(banner, style="bold red")
    console.print("      [dim]>> The Invisible Hand of OSINT <<[/dim]\n")

def list_categories(data):
    """Lists categories (-l command for)"""
    table = Table(title="* Current Categories")
    table.add_column("Category Name", style="cyan")
    table.add_column("Payload Count", style="green")

    for cat, items in data.items():
        table.add_row(cat, str(len(items)))
    
    console.print(table)

def preview_payloads(dorks, category):
    """Lists payloads (-P command for)"""
    table = Table(title=f"$ Preview: [bold green]{category.upper()}[/bold green]")

    table.add_column("ID", justify="center", style="bold yellow", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Raw Payload", style="dim cyan")

    for idx, item in enumerate(dorks, 1):
        table.add_row(str(idx), item['desc'], item['payload'])

    console.print(table)
    console.print("\n[dim]? Tip: Use [bold white]-g 1-5[/bold white] or [bold white]-g 1,3,8[/bold white] to select from this list.[/dim]")

def show_results_table(processed_data):
    """Shows results"""
    table = Table(title="! Prepared Links")

    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Payload", style="green")

    for idx, item in enumerate(processed_data, 1):
        display_id = str(item.get('original_id', idx))
        table.add_row(display_id, item['payload'])

    console.print(table)