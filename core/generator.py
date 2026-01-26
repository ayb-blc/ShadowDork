import urllib.parse

def generate_query(payload, target=None):
    query = ""
    if "{target}" in payload:
        if target:
            query = payload.replace("{target}", target)
        else:
            query = payload.replace("site:{target}", "").strip()
    else:
        if target:
            query = f"site:{target} {payload}"
        else:
            query = payload
    return query

def create_search_url(query, engine="google"):
    """
    Converts the query to the link structure of the selected search engine.
    """
    encoded_query = urllib.parse.quote(query)
    
    if engine == "google":
        return f"https://www.google.com/search?q={encoded_query}"
    elif engine == "ddg" or engine == "duckduckgo":
        # DuckDuckGo loves docks and doesn't ask captchas!
        return f"https://duckduckgo.com/?q={encoded_query}"
    elif engine == "bing":
        return f"https://www.bing.com/search?q={encoded_query}"
    else:
        return f"https://www.google.com/search?q={encoded_query}"