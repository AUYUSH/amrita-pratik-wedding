import time
import json
import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

token = "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"
owner = "AUYUSH"
repo = "amrita-pratik-wedding"

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Wedding-Deployer'
}

print("Background Deployment Listener Started...")
for i in range(120): # 10 minutes
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"🎉 Detected repository '{owner}/{repo}'! Deploying files now...")
            os.system(f'py "C:\\Users\\ayush\\.gemini\antigravity\\scratch\\amrita-pratik-wedding\\deploy_to_github.py" "{token}"')
            sys.exit(0)
    except Exception:
        time.sleep(5)

print("Listener finished 10 minutes window.")
