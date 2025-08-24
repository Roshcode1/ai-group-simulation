from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:3000")

    # Enter a dummy API key
    page.get_by_placeholder("Enter your Gemini API Key").fill("dummy-api-key")

    # Send a message
    page.get_by_placeholder("Type your message...").fill("Hello, who are you?")
    page.get_by_role("button", name="Send").click()

    # Wait for the response
    page.wait_for_selector(".message.user")
    page.wait_for_selector(".message.Alice")

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
