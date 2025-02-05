CF_API_TOKENS = {
    "APIKEY": ["example.com"]
}

def get_api_token(domain_name: str):
    for token, domains in CF_API_TOKENS.items():
        for domain in domains:
            if domain in domain_name:
                return token
