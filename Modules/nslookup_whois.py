import socket
import whois
from datetime import datetime
from Modules.base_scanner import BaseScanner


class NslookupWhois(BaseScanner):
    """
    NSLookup & WHOIS lookup.
    No target restrictions.
    """

    def __init__(self, target):
        super().__init__("NSLookup & WHOIS")
        self.target = target.strip()

    def run(self):
        self.results = []

        # NSLookup
        try:
            ip = socket.gethostbyname(self.target)
            self.results.append(f"🌐 NSLookup Result for {self.target}:")
            self.results.append(f"  - IP Address: {ip}")
        except Exception as e:
            self.results.append(f"❌ NSLookup failed: {e}")

        # WHOIS
        try:
            w = whois.whois(self.target)

            registrar = getattr(w, "registrar", "N/A")
            creation = getattr(w, "creation_date", "N/A")
            updated = getattr(w, "updated_date", "N/A")
            name_servers = getattr(w, "name_servers", [])

            if isinstance(creation, list):
                creation = creation[0]
            if isinstance(creation, datetime):
                creation = creation.strftime("%Y-%m-%d %H:%M:%S")

            if isinstance(updated, list):
                updated = updated[0]
            if isinstance(updated, datetime):
                updated = updated.strftime("%Y-%m-%d %H:%M:%S")

            if isinstance(name_servers, (list, set)):
                name_servers = ", ".join(name_servers)

            self.results.append("📝 WHOIS Information:")
            self.results.append(f"  - Registrar: {registrar}")
            self.results.append(f"  - Creation Date: {creation}")
            self.results.append(f"  - Last Updated: {updated}")
            self.results.append(f"  - Name Servers: {name_servers}")

        except Exception as e:
            self.results.append(f"❌ WHOIS failed: {e}")

        return self.results or ["⚠️ No data found"]
