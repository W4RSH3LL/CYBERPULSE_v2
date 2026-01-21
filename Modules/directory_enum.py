import os
import requests
from urllib.parse import urlparse
from Modules.base_scanner import BaseScanner


class DirectoryEnumerator(BaseScanner):
    """
    Directory enumeration using a wordlist.
    No target restrictions.
    """

    def __init__(self, url, wordlist_path=None):
        super().__init__("Directory Enumeration")
        self.url = self._normalize_url(url)
        self.wordlist_path = wordlist_path or self._default_wordlist()

    # ------------------------
    # Paths
    # ------------------------
    def _base_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    def _default_wordlist(self):
        return os.path.join(self._base_dir(), "wordlists", "directories.txt")

    # ------------------------
    # URL normalization (FIX)
    # ------------------------
    def _normalize_url(self, value: str) -> str:
        value = value.strip()

        # If scheme is missing, default to http
        if not value.startswith(("http://", "https://")):
            value = "http://" + value

        # Remove trailing slash
        return value.rstrip("/")

    # ------------------------
    # Load wordlist
    # ------------------------
    def _load_wordlist(self):
        if not os.path.exists(self.wordlist_path):
            return []

        with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            return [
                "/" + line.strip().lstrip("/")
                for line in f
                if line.strip() and not line.startswith("#")
            ]

    # ------------------------
    # Run
    # ------------------------
    def run(self):
        directories = self._load_wordlist()
        if not directories:
            self.results = ["⚠️ Wordlist not found or empty"]
            return self.results

        for directory in directories:
            try:
                response = requests.get(
                    self.url + directory,
                    timeout=5,
                    allow_redirects=False
                )

                if response.status_code in (200, 301, 302, 403):
                    self.results.append(
                        f"{self.url}{directory} ({response.status_code})"
                    )

            except requests.RequestException:
                continue

        return self.results or ["ℹ️ No directories found"]
