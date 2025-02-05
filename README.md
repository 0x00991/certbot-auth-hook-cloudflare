# Certbot auth/cleanup hook
auth_hook.py, auth_hook_cleanup.py by sonnet  
# 사용법
```bash
sudo certbot certonly -d "*.example.com" -d "example.com" --manual --preferred-challenges dns --manual-auth-hook "python3 /path/to/auth_hook.py" --manual-cleanup-hook "python3 /path/to/auth_hook_cleanup.py"
```