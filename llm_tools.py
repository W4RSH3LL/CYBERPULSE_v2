from Modules.subdomain_enum import SubdomainEnumerator
from Modules.directory_enum import DirectoryEnumerator
from Modules.network_scanner import NetworkScanner
from Modules.nslookup_whois import NslookupWhois


def normalize_url(url: str):
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url


def subdomain_enum(domain: str):
    scanner = SubdomainEnumerator(domain)
    return scanner.run()


def directory_enum(url: str):
    url = normalize_url(url)
    scanner = DirectoryEnumerator(url)
    return scanner.run()


def network_scan():
    scanner = NetworkScanner()
    return scanner.run()


def nslookup_whois(target: str):
    scanner = NslookupWhois(target)
    return scanner.run()


TOOLS = {
    "directory": directory_enum,
    "dir": directory_enum,

    "subdomain": subdomain_enum,
    "subdomains": subdomain_enum,

    "network": network_scan,
    "scan": network_scan,

    "nslookup": nslookup_whois,
    "whois": nslookup_whois,
    "dns": nslookup_whois,
}
