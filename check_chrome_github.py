import os
import shutil
import time
from playwright.sync_api import sync_playwright

chrome_user_data = r"C:\Users\ayush\AppData\Local\Google\Chrome\User Data"
temp_user_data = r"C:\Users\ayush\.gemini\antigravity\scratch\chrome_temp_profile"

if os.path.exists(temp_user_data):
    try:
        shutil.rmtree(temp_user_data)
    except Exception as e:
        print("Cleanup info:", e)

os.makedirs(temp_user_data, exist_ok=True)

# Copy profile folders (Default)
default_dir = os.path.join(chrome_user_data, "Default")
temp_default = os.path.join(temp_user_data, "Default")

if os.path.exists(default_dir):
    print("Copying Chrome Default profile data...")
    os.makedirs(temp_default, exist_ok=True)
    for item in ["Network", "Local Storage", "Cookies", "Web Data"]:
        src = os.path.join(default_dir, item)
        dst = os.path.join(temp_default, item)
        if os.path.exists(src):
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            except Exception as err:
                print(f"Skipping locked file {item}: {err}")

print("Launching Chrome context with copied profile...")
with sync_playwright() as p:
    try:
        context = p.chromium.launch_persistent_context(
            user_data_dir=temp_user_data,
            headless=True,
            channel="chrome",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        page.goto("https://github.com/", wait_until="domcontentloaded")
        time.sleep(3)
        print("Current URL:", page.url)
        content = page.content()
        if "AUYUSH" in content or "dashboard" in page.url or "Sign out" in content or "signed-in" in content:
            print("Successfully authenticated as logged-in user on GitHub!")
        else:
            print("Page title/URL:", page.title(), page.url)
        
        # Navigate to github.com/new
        page.goto("https://github.com/new", wait_until="domcontentloaded")
        time.sleep(2)
        print("Navigated to github.com/new. Screenshotting...")
        page.screenshot(path=r"C:\Users\ayush\.gemini\antigravity\brain\1f5f4726-b9ec-48f7-bf9c-b97190f21454\github_new.png")
        
        # Also check page content on github.com/new
        with open(r"C:\Users\ayush\.gemini\antigravity\scratch\github_new.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        context.close()
    except Exception as e:
        print("Playwright Chrome error:", e)
