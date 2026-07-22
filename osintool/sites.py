import json
import os

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")

class SiteInfo:
    def __init__(self, name, url, url_main, error_type, error_msg=None, error_code=None,
                 request_method="GET", request_payload=None, headers=None, regex_check=None,
                 url_probe=None):
        self.name = name
        self.url = url
        self.url_main = url_main
        self.error_type = error_type
        self.error_msg = error_msg if error_msg else []
        self.error_code = error_code if error_code else []
        self.request_method = request_method.upper()
        self.request_payload = request_payload
        self.headers = headers or {}
        self.regex_check = regex_check
        self.url_probe = url_probe

class SitesLoader:
    def __init__(self, query_type):
        filename = f"{query_type}s.json"
        filepath = os.path.join(RESOURCES_DIR, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "$schema" in data:
            del data["$schema"]

        self.sites = []
        for name, info in data.items():
            self.sites.append(SiteInfo(
                name=name,
                url=info.get("url", ""),
                url_main=info.get("urlMain", ""),
                error_type=info.get("errorType", "status_code"),
                error_msg=info.get("errorMsg", []),
                error_code=info.get("errorCode", []),
                request_method=info.get("request_method", "GET"),
                request_payload=info.get("request_payload"),
                headers=info.get("headers", {}),
                regex_check=info.get("regexCheck"),
                url_probe=info.get("urlProbe"),
            ))

    def __iter__(self):
        return iter(self.sites)

    def __len__(self):
        return len(self.sites)
