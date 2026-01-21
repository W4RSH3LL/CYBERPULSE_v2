import socket
import psutil
from Modules.base_scanner import BaseScanner

class NetworkScanner(BaseScanner):
    known_hosts = set()

    def __init__(self):
        super().__init__("Network Scanner")
        self.alerts = []

    def _guess_device_type(self, hostname):
        h = hostname.lower()
        if "iphone" in h or "android" in h:
            return "phone"
        if "printer" in h:
            return "printer"
        if "tv" in h or "iot" in h:
            return "iot"
        return "computer"

    def run(self):
        discovered = []

        for conn in psutil.net_connections(kind="inet"):
            if conn.raddr:
                ip = conn.raddr.ip
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "Unknown"

                discovered.append({
                    "ip": ip,
                    "hostname": hostname,
                    "type": self._guess_device_type(hostname)
                })

        unique = list({h["ip"]: h for h in discovered}.values())

        for host in unique:
            if host["ip"] not in self.known_hosts:
                self.alerts.append(f"New device detected: {host['ip']}")

        self.known_hosts.update(h["ip"] for h in unique)

        self.results = unique
        return self.results
