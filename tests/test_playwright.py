from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com")
    page.screenshot(path="baidu_homepage.png")
    print("Screenshot saved as baidu_homepage.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)