import subprocess
import time
from playwright.sync_api import sync_playwright

print("Starting Chrome with remote debugging port 9222...")
cmd = r'start "" "chrome.exe" --remote-debugging-port=9222 "https://github.com/new"'
subprocess.Popen(cmd, shell=True)
time.sleep(3)

with sync_playwright() as p:
    try:
        print("Connecting Playwright over CDP to localhost:9222...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        print("Connected successfully!")
        
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        print("Current page URL:", page.url)
        page.goto("https://github.com/new", wait_until="domcontentloaded")
        time.sleep(2)
        print("Page title:", page.title())
        
        # Check if logged in on GitHub
        content = page.content()
        if "Repository name" in content or "create-repo" in content or "Create a new repository" in page.title():
            print("Successfully accessed GitHub Create Repository page!")
            
            # Fill repository name
            name_input = page.locator("input[aria-label='Repository name'], input[name='repository[name]'], input[data-testid='repository-name-input']").first
            if name_input.count() > 0:
                print("Filling repository name 'amrita-pratik-wedding'...")
                name_input.fill("amrita-pratik-wedding")
                time.sleep(2)
                
            # Check README if present
            readme = page.locator("input[name='repository[auto_init]'], #repository_auto_init").first
            if readme.count() > 0 and not readme.is_checked():
                print("Checking README checkbox...")
                readme.check(force=True)
                time.sleep(1)
                
            # Click Create repository button
            create_btn = page.locator("button:has-text('Create repository'), input[type='submit'][value='Create repository']").first
            if create_btn.count() > 0:
                print("Clicking Create repository button...")
                create_btn.click(force=True)
                time.sleep(5)
                print("Created! New URL:", page.url)
                
        else:
            print("Page content preview:", page.title())
            
    except Exception as e:
        print("CDP Connection info:", e)
