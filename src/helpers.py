def create_manifest_url(domain: str):
    return "https://{domain}/.well-known/ai-plugin.json".format(domain=domain)
