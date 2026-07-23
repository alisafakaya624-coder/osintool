import os
import time
from colorama import Fore, Style


class InstagramAuth:
    def __init__(self, credentials):
        self.creds = credentials
        self.client = None
        self.visited = set()
        self.graph = {}
        self._user_counter = 0

    def search(self, target, depth=2, max_per_level=5):
        from instagrapi import Client
        from instagrapi.exceptions import LoginRequired

        self._root_user = target
        cl = Client()
        self.client = cl
        u = self.creds["username"]
        p = self.creds["password"]

        print(f"{Fore.CYAN}[Instagram] Logging in as @{u}...{Style.RESET_ALL}")
        cl.login(u, p)

        self._crawl(target, depth=depth, max_per_level=max_per_level)
        self._print_graph(target)
        self._generate_report_if_needed(force=True)
        return self.graph

    def _crawl(self, username, depth=2, max_per_level=5):
        if username in self.visited or depth < 0:
            return
        self.visited.add(username)

        try:
            user_id = self.client.user_id_from_username(username)
            info = self.client.user_info(user_id)
        except Exception as e:
            print(f"{Fore.RED}[!] @{username}: {e}{Style.RESET_ALL}")
            return

        indent = "  " * (2 - depth)
        print(f"\n{indent}{Fore.CYAN}@{username}{Style.RESET_ALL} ({info.full_name or '-'}) "
              f"{Fore.YELLOW}[{info.follower_count}F / {info.following_count}FG]{Style.RESET_ALL}")

        self.graph[username] = {
            "id": user_id,
            "full_name": info.full_name or "",
            "followers": info.follower_count,
            "following": info.following_count,
            "is_private": info.is_private,
            "is_verified": info.is_verified,
            "bio": info.biography or "",
            "follower_list": [],
            "following_list": [],
            "url": f"https://instagram.com/{username}",
        }

        self._user_counter += 1
        self._generate_report_if_needed()

        if depth <= 1:
            return

        time.sleep(1)

        try:
            followers = self.client.user_followers(user_id, amount=max_per_level)
            for uid, uinfo in followers.items():
                f_username = uinfo.username
                self.graph[username]["follower_list"].append(f_username)
                print(f"{indent}  {Fore.GREEN}Takiptekiler:{Style.RESET_ALL} @{f_username}")
                self._crawl(f_username, depth - 1, max_per_level)
        except Exception as e:
            print(f"{indent}  {Fore.RED}[!] Followers error: {e}{Style.RESET_ALL}")

        time.sleep(1)

        try:
            following = self.client.user_following(user_id, amount=max_per_level)
            for uid, uinfo in following.items():
                f_username = uinfo.username
                self.graph[username]["following_list"].append(f_username)
                print(f"{indent}  {Fore.BLUE}Takip ettikleri:{Style.RESET_ALL} @{f_username}")
                self._crawl(f_username, depth - 1, max_per_level)
        except Exception as e:
            print(f"{indent}  {Fore.RED}[!] Following error: {e}{Style.RESET_ALL}")

    def _generate_report_if_needed(self, force=False):
        if not force and self._user_counter % 200 != 0:
            return
        if not self.graph:
            return
        try:
            from ..report import generate_report
            output_dir = os.path.expanduser("~")
            generate_report(self.graph, self._root_user, output_dir=output_dir)
        except Exception as e:
            print(f"{Fore.RED}[!] PDF rapor hatasi: {e}{Style.RESET_ALL}")

    def _print_graph(self, root):
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  BAĞLANTI GRAFİ - @{root}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")

        for user, data in self.graph.items():
            print(f"\n{Fore.CYAN}@{user}{Style.RESET_ALL}")
            print(f"  İsim     : {data['full_name'] or '-'}")
            print(f"  Bio      : {data['bio'][:80] or '-'}")
            print(f"  Takipçi  : {data['followers']}")
            print(f"  Takip    : {data['following']}")
            if data["is_private"]:
                print(f"  🔒 Gizli hesap")

            if data["follower_list"]:
                print(f"  {Fore.GREEN}Takiptekiler ({len(data['follower_list'])}):{Style.RESET_ALL}")
                for f in data["follower_list"]:
                    mutual = ""
                    if f in self.graph:
                        mutual = f" {Fore.YELLOW}(grafikte var){Style.RESET_ALL}"
                    print(f"    - @{f}{mutual}")

            if data["following_list"]:
                print(f"  {Fore.BLUE}Takip ettikleri ({len(data['following_list'])}):{Style.RESET_ALL}")
                for f in data["following_list"]:
                    mutual = ""
                    if f in self.graph:
                        mutual = f" {Fore.YELLOW}(grafikte var){Style.RESET_ALL}"
                    print(f"    - @{f}{mutual}")

        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Toplam {len(self.graph)} kullanıcı tarandı{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
