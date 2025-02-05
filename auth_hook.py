import os
import sys
import time
import requests
from tokens import get_api_token

# CloudFlare API 설정
CF_API_URL = "https://api.cloudflare.com/client/v4"

def get_zone_id(domain):
    CF_API_TOKEN = get_api_token(domain)
    parts = domain.split('.')
    zone_name = '.'.join(parts[-2:])
    
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{CF_API_URL}/zones",
        headers=headers,
        params={"name": zone_name}
    )
    
    if not response.ok:
        raise Exception(f"Failed to get zone ID: {response.text}")
    
    data = response.json()
    if not data["success"] or not data["result"]:
        raise Exception(f"Zone not found for domain: {domain}")
    
    return data["result"][0]["id"]

def add_dns_record(certbot_domain, certbot_validation):
    CF_API_TOKEN = get_api_token(certbot_domain)

    try:
        # 도메인 정보 준비
        record_name = f'_acme-challenge.{certbot_domain}'
        
        # Zone ID 가져오기
        zone_id = get_zone_id(certbot_domain)
        
        # API 요청 헤더
        headers = {
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # DNS 레코드 생성
        data = {
            "type": "TXT",
            "name": record_name,
            "content": certbot_validation,
            "ttl": 120
        }
        
        response = requests.post(
            f"{CF_API_URL}/zones/{zone_id}/dns_records",
            headers=headers,
            json=data
        )
        
        if not response.ok:
            raise Exception(f"Failed to add DNS record: {response.text}")
        
        # DNS 전파 대기
        print("Waiting for DNS propagation...")
        time.sleep(30)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    domain = os.environ.get('CERTBOT_DOMAIN')
    validation = os.environ.get('CERTBOT_VALIDATION')

    if not domain or not validation:
        print("Required environment variables CERTBOT_DOMAIN or CERTBOT_VALIDATION are missing", 
              file=sys.stderr)
        sys.exit(1)

    add_dns_record(domain, validation)