import requests
from colorama import Fore, Style


def search_github(query, limit=10):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "osintool/1.0",
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data.get("items", [])
    except Exception:
        return None


def format_repo(repo):
    name = repo["full_name"]
    stars = repo["stargazers_count"]
    desc = repo.get("description") or "(aciklama yok)"
    lang = repo.get("language") or "-"
    url = repo["html_url"]
    topics = ", ".join(repo.get("topics", [])[:5])

    output = f"{Fore.CYAN}{name}{Style.RESET_ALL}"
    output += f"\n  {Fore.YELLOW}{stars} ★{Style.RESET_ALL}  {Fore.GREEN}{lang}{Style.RESET_ALL}"
    if topics:
        output += f"  {Fore.BLUE}[{topics}]{Style.RESET_ALL}"
    output += f"\n  {desc[:120]}"
    output += f"\n  {Fore.MAGENTA}{url}{Style.RESET_ALL}"
    return output
