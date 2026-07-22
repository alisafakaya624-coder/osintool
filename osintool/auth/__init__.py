from colorama import Fore, Style

from .config import AuthConfig
from .instagram import InstagramAuth
from .github import GitHubAuth
from .reddit import RedditAuth
from .whatsapp import WhatsAppAuth
from .telegram import TelegramAuth


MODULES = {
    "instagram": InstagramAuth,
    "github": GitHubAuth,
    "reddit": RedditAuth,
    "whatsapp": WhatsAppAuth,
    "telegram": TelegramAuth,
}


def search_target(target, platforms=None, depth=2, max_per_level=5):
    cfg = AuthConfig()
    if not cfg.exists() and "whatsapp" not in (platforms or []):
        print(f"{Fore.RED}[!] No auth config found. Run: osintool --auth-config --set-<platform>{Style.RESET_ALL}")
        return

    if platforms:
        platform_list = [p for p in platforms if p in MODULES]
    else:
        platform_list = list(MODULES.keys())

    for name in platform_list:
        if name == "whatsapp":
            mod = MODULES[name]()
            try:
                result = mod.search(target)
            except Exception as e:
                print(f"{Fore.RED}[!] {name}: {e}{Style.RESET_ALL}")
            continue

        if name == "instagram":
            mod = MODULES[name](cfg.get(name) or {})
            try:
                result = mod.search(target, depth=depth, max_per_level=max_per_level)
            except Exception as e:
                print(f"{Fore.RED}[!] {name}: {e}{Style.RESET_ALL}")
            continue

        creds = cfg.get(name)
        if not creds:
            print(f"{Fore.YELLOW}[-] {name}: no credentials configured, skipping{Style.RESET_ALL}")
            continue
        mod = MODULES[name](creds)
        try:
            result = mod.search(target)
        except Exception as e:
            print(f"{Fore.RED}[!] {name}: {e}{Style.RESET_ALL}")
            continue


def cmd_auth_config(args):
    cfg = AuthConfig()
    if args.set_instagram:
        u = input("Instagram username: ").strip()
        p = input("Instagram password: ").strip()
        cfg.set("instagram", {"username": u, "password": p})
        cfg.save()
        print(f"{Fore.GREEN}[+] Instagram credentials saved{Style.RESET_ALL}")
    elif args.set_github:
        t = input("GitHub personal access token: ").strip()
        cfg.set("github", {"token": t})
        cfg.save()
        print(f"{Fore.GREEN}[+] GitHub credentials saved{Style.RESET_ALL}")
    elif args.set_reddit:
        cid = input("Reddit client_id: ").strip()
        cs = input("Reddit client_secret: ").strip()
        u = input("Reddit username: ").strip()
        p = input("Reddit password: ").strip()
        cfg.set("reddit", {"client_id": cid, "client_secret": cs, "username": u, "password": p})
        cfg.save()
        print(f"{Fore.GREEN}[+] Reddit credentials saved{Style.RESET_ALL}")
    elif args.set_telegram:
        phone = input("Telegram phone (e.g. +905551234567): ").strip()
        api_id = input("Telegram API ID (or ENTER to skip): ").strip()
        api_hash = input("Telegram API Hash (or ENTER to skip): ").strip()
        data = {"phone": phone}
        if api_id:
            data["api_id"] = api_id
        if api_hash:
            data["api_hash"] = api_hash
        cfg.set("telegram", data)
        cfg.save()
        print(f"{Fore.GREEN}[+] Telegram credentials saved{Style.RESET_ALL}")
    elif args.list_auth:
        platforms = cfg.list_platforms()
        if not platforms:
            print(f"{Fore.YELLOW}[*] No credentials configured{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}[*] Configured platforms: {', '.join(platforms)}{Style.RESET_ALL}")
    return cfg
