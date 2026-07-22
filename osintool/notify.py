from colorama import Fore, Style
from .result import QueryStatus

class QueryNotify:
    def start(self, message):
        pass

    def update(self, result):
        pass

    def finish(self):
        pass

class QueryNotifyPrint(QueryNotify):
    def __init__(self, print_all=False, no_color=False):
        self.print_all = print_all
        self.no_color = no_color
        self.found_count = 0
        self.total_count = 0

    def start(self, query_type, query):
        msg = f"{query_type.upper()} search for: {query}"
        print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} {msg}")
        print()

    def update(self, result):
        self.total_count += 1
        if result.status == QueryStatus.CLAIMED:
            self.found_count += 1
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {result.site_name}: {Fore.CYAN}{result.site_url_user}{Style.RESET_ALL}")
        elif result.status == QueryStatus.ILLEGAL:
            print(f"{Fore.YELLOW}[-]{Style.RESET_ALL} {result.site_name}: Illegal Format")
        elif result.status == QueryStatus.UNKNOWN:
            ctx = result.context or "Unknown"
            print(f"{Fore.RED}[-]{Style.RESET_ALL} {result.site_name}: {ctx}")
        elif self.print_all:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} {result.site_name}: Not Found!")

    def finish(self):
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Found on {self.found_count}/{self.total_count} sites")
