# Certbot auth/cleanup hook (Cloudflare)
auth_hook.py, auth_hook_cleanup.py by sonnet  
dns 챌린지를 위한 TXT 레코드 생성을 자동화해주는 스크립트입니다. tokens.py 파일을 수정 후 사용해주세요.  
# 사용법
```bash
sudo certbot certonly -d "*.example.com" -d "example.com" --manual --preferred-challenges dns --manual-auth-hook "python3 /path/to/auth_hook.py" --manual-cleanup-hook "python3 /path/to/auth_hook_cleanup.py"
```
