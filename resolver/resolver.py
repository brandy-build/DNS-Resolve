import dns.resolver


def resolve(domain):
    result = {}
    try:
        a = dns.resolver.resolve(domain, 'A')
        result['A'] = [r.to_text() for r in a]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        result['A'] = []

    try:
        aaaa = dns.resolver.resolve(domain, 'AAAA')
        result['AAAA'] = [r.to_text() for r in aaaa]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        result['AAAA'] = []

    try:
        mx = dns.resolver.resolve(domain, 'MX')
        result['MX'] = [r.to_text() for r in mx]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        result['MX'] = []

    return result


if __name__ == "__main__":
    print(resolve("example.com"))
