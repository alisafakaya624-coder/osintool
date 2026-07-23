import argparse
import json
import os
import re
import sys
import time
from urllib.parse import quote

import requests
from colorama import Fore, Style, init as colorama_init

from .result import QueryResult, QueryStatus
from .notify import QueryNotifyPrint
from .sites import SitesLoader
from .crypto import save_encrypted, STORAGE_FILE as FOUNDS_FILE


def build_url(template, query):
    return template.replace("{}", quote(query, safe=""))


def check_site(site, query, session, timeout):
    url = build_url(site.url, query)
    probe_url = build_url(site.url_probe, query) if site.url_probe else url

    if site.regex_check:
        if not re.match(site.regex_check, query):
            return QueryResult(query, site.name, url, QueryStatus.ILLEGAL)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    if site.headers:
        headers.update(site.headers)

    try:
        start = time.time()
        if site.request_method == "POST":
            payload = site.request_payload
            if payload:
                payload_str = json.dumps(payload).replace("{}", query)
                payload = json.loads(payload_str)
            resp = session.post(probe_url, json=payload, headers=headers, timeout=timeout, allow_redirects=False)
        elif site.request_method == "HEAD":
            resp = session.head(probe_url, headers=headers, timeout=timeout, allow_redirects=False)
        else:
            resp = session.get(probe_url, headers=headers, timeout=timeout, allow_redirects=False)

        elapsed = time.time() - start

        if site.error_type == "status_code":
            error_codes = site.error_code or [404, 403, 410, 301]
            if resp.status_code in error_codes:
                return QueryResult(query, site.name, url, QueryStatus.AVAILABLE, elapsed)
            return QueryResult(query, site.name, url, QueryStatus.CLAIMED, elapsed)

        elif site.error_type == "message":
            body = resp.text.lower()
            for msg in site.error_msg:
                if msg.lower() in body:
                    return QueryResult(query, site.name, url, QueryStatus.AVAILABLE, elapsed)
            if resp.status_code in (404, 410):
                return QueryResult(query, site.name, url, QueryStatus.AVAILABLE, elapsed)
            return QueryResult(query, site.name, url, QueryStatus.CLAIMED, elapsed)

        elif site.error_type == "response_url":
            if resp.url.rstrip("/") != probe_url.rstrip("/"):
                return QueryResult(query, site.name, url, QueryStatus.AVAILABLE, elapsed)
            return QueryResult(query, site.name, url, QueryStatus.CLAIMED, elapsed)

        else:
            return QueryResult(query, site.name, url, QueryStatus.UNKNOWN, elapsed, f"Unknown errorType: {site.error_type}")

    except requests.exceptions.Timeout:
        return QueryResult(query, site.name, url, QueryStatus.UNKNOWN, context="Timeout")
    except requests.exceptions.ConnectionError:
        return QueryResult(query, site.name, url, QueryStatus.UNKNOWN, context="Connection Error")
    except Exception as e:
        return QueryResult(query, site.name, url, QueryStatus.UNKNOWN, context=str(e)[:50])


def search(query_type, query, notifier, timeout=30):
    loader = SitesLoader(query_type)
    notifier.start(query_type, query)
    notifier.total_count = len(loader.sites)

    session = requests.Session()
    results = []
    for site in loader.sites:
        result = check_site(site, query, session, timeout)
        notifier.update(result)
        results.append(result)

    notifier.finish()
    return results


def main():
    colorama_init(autoreset=True)
    parser = argparse.ArgumentParser(
        description="OSINTool - Search usernames, names, and phone numbers across platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  osintool -u username          # username search
  osintool -n "John Doe"        # name search
  osintool -p "+14155552671"    # phone search
  osintool -u -n "John Smith"   # name search (alternative)
  osintool --all "query"        # try all 3 types with the same query
        """,
    )

    parser.add_argument("query", nargs="?", help="Search query (username, name, or phone)")
    parser.add_argument("-u", "--username", metavar="USERNAME", help="Search by username")
    parser.add_argument("-n", "--name", metavar="NAME", help="Search by full name")
    parser.add_argument("-p", "--phone", metavar="PHONE", help="Search by phone number")
    parser.add_argument("--all", metavar="QUERY", help="Search all types with the same query")
    parser.add_argument("--print-all", action="store_true", help="Show sites where not found")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--auth", metavar="TARGET", help="Authenticated search: login to platforms and search target")
    parser.add_argument("--auth-platforms", metavar="PLATFORMS", nargs="+",
                        choices=["instagram", "github", "reddit", "whatsapp", "telegram", "all"], default=["all"],
                        help="Platforms to use with --auth")
    parser.add_argument("--auth-depth", type=int, default=2,
                        help="Recursion depth for Instagram follower graph (default: 2)")
    parser.add_argument("--auth-max", type=int, default=5,
                        help="Max followers/following to crawl per level (default: 5)")
    parser.add_argument("--auth-config", action="store_true", help="Manage auth credentials")
    parser.add_argument("--set-instagram", action="store_true", help="Set Instagram credentials")
    parser.add_argument("--set-github", action="store_true", help="Set GitHub credentials")
    parser.add_argument("--set-reddit", action="store_true", help="Set Reddit credentials")
    parser.add_argument("--set-telegram", action="store_true", help="Set Telegram phone number")
    parser.add_argument("--list-auth", action="store_true", help="List configured platforms")
    parser.add_argument("--gh-search", metavar="QUERY", help="Search GitHub repos by keyword (no login needed)")

    args = parser.parse_args()

    if args.gh_search:
        from .github_search import search_github, format_repo
        items = search_github(args.gh_search, limit=10)
        if items is None:
            print(f"{Fore.RED}[!] GitHub API hatasi veya rate limit{Style.RESET_ALL}")
        elif not items:
            print(f"{Fore.YELLOW}[-] Sonuc bulunamadi{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}{'='*65}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}  GitHub - En cok yildiz alan repolar: '{args.gh_search}'{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*65}{Style.RESET_ALL}")
            for i, repo in enumerate(items, 1):
                print(f"\n{Fore.YELLOW}[{i:02d}]{Style.RESET_ALL} {format_repo(repo)}")
            print(f"\n{Fore.GREEN}{'='*65}{Style.RESET_ALL}")
        return 0

    if args.auth_config:
        from .auth import cmd_auth_config
        cmd_auth_config(args)
        return 0

    if args.auth:
        from .auth import search_target
        platforms = [p for p in args.auth_platforms if p != "all"] if args.auth_platforms else None
        kwargs = {"depth": args.auth_depth, "max_per_level": args.auth_max}
        search_target(args.auth, platforms, **kwargs)
        return 0

    queries = []
    if args.username:
        queries.append(("username", args.username))
    if args.name:
        queries.append(("name", args.name))
    if args.phone:
        queries.append(("phone", args.phone))
    if args.all:
        for t in ("username", "name", "phone"):
            queries.append((t, args.all))
    if args.query and not any([args.username, args.name, args.phone, args.all]):
        queries.append(("username", args.query))

    if not queries:
        parser.print_help()
        sys.exit(1)

    notifier = QueryNotifyPrint(print_all=args.print_all, no_color=args.no_color)
    results = {}
    for qtype, q in queries:
        result = search(qtype, q, notifier, timeout=args.timeout)
        results[qtype] = result
        print()

    founds = {}
    for qtype, q in queries:
        found_list = []
        for r in results.get(qtype, []):
            if r.status == QueryStatus.CLAIMED:
                found_list.append({"site": r.site_name, "url": r.site_url_user})
        if found_list:
            founds[qtype] = {"query": q, "sites": found_list}

    if founds:
        founds["_meta"] = {"queries": len(queries)}
        PASSWORD = os.environ.get("OSINTOOL_PASSWORD", "osintool_default_change_me")
        save_encrypted(founds, PASSWORD)
        print(f"{Fore.GREEN}[+] Saved encrypted results to {FOUNDS_FILE}{Style.RESET_ALL}")

    return 0


if __name__ == "__main__":
    main()
