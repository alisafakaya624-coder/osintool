from enum import Enum

class QueryStatus(Enum):
    CLAIMED = "Claimed"
    AVAILABLE = "Available"
    UNKNOWN = "Unknown"
    ILLEGAL = "Illegal"

class QueryResult:
    def __init__(self, query, site_name, site_url, status, query_time=None, context=None):
        self.query = query
        self.site_name = site_name
        self.site_url_user = site_url
        self.status = status
        self.query_time = query_time
        self.context = context

    def __str__(self):
        status_str = self.status.value
        if self.context:
            return f"{status_str} ({self.context})"
        return status_str
