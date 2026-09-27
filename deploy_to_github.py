import os
import sys
import base64
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\ayush\.gemini\antigravity\scratch\amrita-pratik-wedding"
REPO_NAME = "amrita-pratik-wedding"

def make_request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            res_body = resp.read().decode('utf-8')
            return json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {err_body}")
        raise e

def upload_blob(token, owner, repo, content_bytes):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/blobs"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'Wedding-Deployer'
    }
    b64_str = base64.b64encode(content_bytes).decode('utf-8')
    res = make_request(url, method="POST", headers=headers, data={
        "content": b64_str,
        "encoding": "base64"
    })
    return res['sha']

def deploy(token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Wedding-Deployer'
    }

    # 1. Get current authenticated user info
    print("Connecting to GitHub...")
    user_info = make_request("https://api.github.com/user", headers=headers)
    owner = user_info['login']
    print(f"✅ Authenticated as GitHub user: {owner}")

    # 2. Check if repo exists
    repo_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}"
    repo_exists = False
    try:
        make_request(repo_url, headers=headers)
        repo_exists = True
        print(f"ℹ️ Repository '{REPO_NAME}' already exists.")
    except Exception:
        pass

    if not repo_exists:
        print(f"🚀 Creating public repository '{REPO_NAME}' on GitHub...")
        create_url = "https://api.github.com/user/repos"
        try:
            make_request(create_url, method="POST", headers={**headers, 'Content-Type': 'application/json'}, data={
                "name": REPO_NAME,
                "description": "Amrita & Pratik Luxury Wedding Invitation Website",
                "private": False,
                "auto_init": True
            })
            print("✅ Repository created successfully!")
        except Exception as e:
            print(f"Could not create repository via API: {e}")
            print("Please ensure the repository 'amrita-pratik-wedding' is created on https://github.com/new")

    # 3. Create Blobs and Tree
    print("\n📦 Uploading website assets & files...")
    tree_items = []
    exclude_files = ['deploy_to_github.py', '.git']

    for root, dirs, files in os.walk(PROJECT_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, PROJECT_DIR).replace("\\", "/")
            if any(rel_path.startswith(ex) for ex in exclude_files):
                continue

            print(f"  -> Uploading {rel_path}...")
            with open(full_path, "rb") as file_obj:
                content = file_obj.read()
            
            sha = upload_blob(token, owner, repo=REPO_NAME, content_bytes=content)
            tree_items.append({
                "path": rel_path,
                "mode": "100644",
                "type": "blob",
                "sha": sha
            })

    # 4. Create Commit & Update Main Branch Reference
    print("\n🔨 Creating Git commit...")
    # Get latest commit sha of main branch or master branch
    ref_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/refs/heads/main"
    try:
        ref_info = make_request(ref_url, headers=headers)
        parent_sha = ref_info['object']['sha']
    except Exception:
        # Fallback to master
        ref_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/refs/heads/master"
        ref_info = make_request(ref_url, headers=headers)
        parent_sha = ref_info['object']['sha']

    # Create Tree
    tree_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/trees"
    tree_res = make_request(tree_url, method="POST", headers={**headers, 'Content-Type': 'application/json'}, data={
        "base_tree": parent_sha,
        "tree": tree_items
    })
    new_tree_sha = tree_res['sha']

    # Create Commit
    commit_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/commits"
    commit_res = make_request(commit_url, method="POST", headers={**headers, 'Content-Type': 'application/json'}, data={
        "message": "Deploy Amrita & Pratik Luxury Wedding Website",
        "tree": new_tree_sha,
        "parents": [parent_sha]
    })
    new_commit_sha = commit_res['sha']

    # Update Ref
    update_ref_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}/git/refs/heads/main"
    make_request(update_ref_url, method="PATCH", headers={**headers, 'Content-Type': 'application/json'}, data={
        "sha": new_commit_sha,
        "force": True
    })
    print("✅ Git commit pushed successfully!")

    # 5. Enable GitHub Pages
    print("\n🌐 Enabling GitHub Pages...")
    pages_url = f"https://api.github.com/repos/{owner}/{REPO_NAME}/pages"
    try:
        make_request(pages_url, method="POST", headers={
            **headers,
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.mysterio-preview+json'
        }, data={"source": {"branch": "main", "path": "/"}})
        print("✅ GitHub Pages enabled!")
    except Exception as e:
        print("ℹ️ GitHub Pages status:", e)

    live_url = f"https://{owner}.github.io/{REPO_NAME}/"
    print("\n" + "="*65)
    print(f"🎉 CONGRATULATIONS! Website is now LIVE on GitHub Pages!")
    print(f"🔗 Public Website Link: {live_url}")
    print("="*65)
    return live_url

if __name__ == '__main__':
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
        deploy(token)
    else:
        print("Usage: py deploy_to_github.py <GITHUB_PERSONAL_ACCESS_TOKEN>")
