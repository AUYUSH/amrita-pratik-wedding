import json
import urllib.request

token = "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"
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Wedding-Deployer'
}

req = urllib.request.Request("https://api.github.com/user/repos", headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        repos = json.loads(resp.read().decode('utf-8'))
        print("Accessible Repositories:")
        for r in repos:
            print(" -", r['full_name'])
except Exception as e:
    print("Error listing repos:", e)
