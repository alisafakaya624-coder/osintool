from colorama import Fore, Style


class GitHubAuth:
    def __init__(self, credentials):
        self.token = credentials["token"]

    def search(self, target):
        from github import Github

        g = Github(self.token)

        print(f"{Fore.CYAN}[GitHub] Searching for @{target}...{Style.RESET_ALL}")
        try:
            u = g.get_user(target)
            u.login
        except Exception:
            print(f"{Fore.RED}[!] User @{target} not found on GitHub{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[GitHub] @{target}{Style.RESET_ALL}")
        print(f"{'='*50}")
        print(f"  Name      : {u.name or '-'}")
        print(f"  Bio       : {u.bio or '-'}")
        print(f"  Company   : {u.company or '-'}")
        print(f"  Location  : {u.location or '-'}")
        print(f"  Email     : {u.email or '-'}")
        print(f"  Blog      : {u.blog or '-'}")
        print(f"  Twitter   : @{u.twitter_username or '-'}")
        print(f"  Repos     : {u.public_repos}")
        print(f"  Gists     : {u.public_gists}")
        print(f"  Followers : {u.followers}")
        print(f"  Following : {u.following}")
        print(f"  Created   : {u.created_at.strftime('%Y-%m-%d')}")
        print(f"  Profile   : https://github.com/{target}")
        print(f"{'='*50}")

        repos = u.get_repos(type="public", sort="updated", direction="desc")
        print(f"{Fore.YELLOW}[*] Recent repos:{Style.RESET_ALL}")
        for i, r in enumerate(repos):
            if i >= 5:
                break
            desc = (r.description or "")[:80]
            lang = r.language or "-"
            print(f"    - {r.name}: {desc} [{lang}]")

        return {"username": target, "info": str(u)}
