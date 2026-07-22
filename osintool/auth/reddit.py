from colorama import Fore, Style


class RedditAuth:
    def __init__(self, credentials):
        self.creds = credentials

    def search(self, target):
        import praw

        reddit = praw.Reddit(
            client_id=self.creds["client_id"],
            client_secret=self.creds["client_secret"],
            username=self.creds["username"],
            password=self.creds["password"],
            user_agent="osintool:v1.0 (by /u/" + self.creds["username"] + ")",
        )

        print(f"{Fore.CYAN}[Reddit] Searching for u/{target}...{Style.RESET_ALL}")
        try:
            u = reddit.redditor(target)
            u.name
        except Exception:
            print(f"{Fore.RED}[!] User u/{target} not found on Reddit{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[Reddit] u/{target}{Style.RESET_ALL}")
        print(f"{'='*50}")
        print(f"  Created   : {u.created_utc and 'Yes' or '-'}")

        try:
            created = u.created_utc
            from datetime import datetime
            print(f"  Account age: {datetime.fromtimestamp(created).strftime('%Y-%m-%d')}")
        except Exception:
            pass

        print(f"  Link Karma: {u.link_karma}")
        print(f"  Comment Kr: {u.comment_karma}")
        print(f"  Profile    : https://reddit.com/u/{target}")
        print(f"{'='*50}")

        print(f"{Fore.YELLOW}[*] Recent posts:{Style.RESET_ALL}")
        for i, post in enumerate(u.submissions.new(limit=5)):
            sub = post.subreddit.display_name
            title = post.title[:80]
            score = post.score
            print(f"    - r/{sub}: {title} ({score} pts)")

        print(f"{Fore.YELLOW}[*] Recent comments:{Style.RESET_ALL}")
        for i, comment in enumerate(u.comments.new(limit=5)):
            sub = comment.subreddit.display_name
            body = comment.body[:80].replace("\n", " ")
            score = comment.score
            print(f"    - r/{sub}: {body} ({score} pts)")

        return {"username": target, "info": str(u)}
