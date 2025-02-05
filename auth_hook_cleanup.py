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

def cleanup_dns_record(certbot_domain, certbot_validation):
    CF_API_TOKEN = get_api_token(certbot_domain)
    """DNS TXT 레코드를 삭제합니다."""
    try:
        zone_id = get_zone_id(certbot_domain)
        record_name = f'_acme-challenge.{certbot_domain}'
        
        headers = {
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # DNS 레코드 목록 조회
        response = requests.get(
            f"{CF_API_URL}/zones/{zone_id}/dns_records",
            headers=headers,
            params={"type": "TXT", "name": record_name}
        )
        
        if not response.ok:
            raise Exception(f"Failed to get DNS records: {response.text}")
        
        records = response.json()["result"]
        for record in records:
            if record["content"] == certbot_validation:
                # 일치하는 레코드 삭제
                delete_response = requests.delete(
                    f"{CF_API_URL}/zones/{zone_id}/dns_records/{record['id']}",
                    headers=headers
                )
                if not delete_response.ok:
                    raise Exception(f"Failed to delete DNS record: {delete_response.text}")
                break
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Certbot에서 전달하는 환경 변수 확인
    domain = os.environ.get('CERTBOT_DOMAIN')
    validation = os.environ.get('CERTBOT_VALIDATION')

    if not domain or not validation:
        print("Required environment variables CERTBOT_DOMAIN or CERTBOT_VALIDATION are missing", 
              file=sys.stderr)
        sys.exit(1)

    cleanup_dns_record(domain, validation)