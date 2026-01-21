import os
import dns.resolver
from urllib.parse import urlparse
from Modules.base_scanner import BaseScanner


class SubdomainEnumerator(BaseScanner):
    """
    Subdomain enumeration using DNS resolution and a wordlist.
    No target restrictions.
    """

    def __init__(self, domain, wordlist_path=None):
        super().__init__("Subdomain Enumeration")
        self.domain = self._normalize_domain(domain)
        self.wordlist_path = wordlist_path or self._default_wordlist()

    # ------------------------
    # Paths
    # ------------------------
    def _base_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    def _default_wordlist(self):
        return os.path.join(self._base_dir(), "wordlists", "subdomains.txt")

    # ------------------------
    # Normalize domain
    # ------------------------
    def _normalize_domain(self, value: str) -> str:
        value = value.strip().lower()

        if value.startswith(("http://", "https://")):
            parsed = urlparse(value)
            value = parsed.hostname or value

        return value.rstrip("/")

    # ------------------------
    # Load wordlist
    # ------------------------
    def _load_wordlist(self):
        if not os.path.exists(self.wordlist_path):
            return []

        with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            return [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

    # ------------------------
    # Run
    # ------------------------
    def run(self):
        subdomains = self._load_wordlist()
        if not subdomains:
            self.results = ["⚠️ Wordlist not found or empty"]
            return self.results

        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 2

        for sub in subdomains:
            fqdn = f"{sub}.{self.domain}"
            try:
                resolver.resolve(fqdn, "A")
                self.results.append(fqdn)
            except (
                dns.resolver.NoAnswer,
                dns.resolver.NXDOMAIN,
                dns.resolver.Timeout,
                dns.resolver.NoNameservers
            ):
                continue

        return self.results or ["ℹ️ No subdomains found"]
