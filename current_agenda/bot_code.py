from typing import Any
import cloudscraper
import os
from dotenv import load_dotenv
from weasyprint import HTML
import time
import random



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By


def generate_pdf(html_response: Any, output_file:str = "agenda.pdf")-> None:
    # Convert HTML content to PDF
    HTML(string=html_response.text).write_pdf(output_file)

def get_screenshot():
    #Todo figure out how to use chrome for testing with selenium
    # Path to the Chrome for Testing binary and ChromeDriver
    chrome_driver_path = "../chrome-for-testing/chromedriver-mac-arm64/chromedriver"
    chrome_binary_path = "../chrome-for-testing/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

    # Set up Selenium WebDriver with Chrome for Testing
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary_path  # Use the Chrome for Testing binary
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")  # Default window size
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


    # Start WebDriver with Chrome for Testing driver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        # Navigate to the desired webpage
        url = "https://easy-speak.org/viewagenda.php?t=586027&pr=1"  # Replace with your target URL
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Wait for 2-5 seconds randomly

        # Get the total height of the page
        total_height = driver.execute_script("return document.body.scrollHeight")

        # Set the window size to capture the full page
        driver.set_window_size(1920, total_height)

        # Capture full-page screenshot
        screenshot_path = "full_page_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"Full-page screenshot saved as {screenshot_path}")

    finally:
        # Clean up and close the driver
        driver.quit()


if __name__ == "__main__":

    # Create a cloudscraper instance
    scraper = cloudscraper.create_scraper()

    # Load variables from the .env file
    load_dotenv()

    # Login URL and credentials
    login_url = "https://easy-speak.org/login.php"
    login_payload = {
        "username": os.getenv("EASY_SPEAK_USERNAME"),
        "password": os.getenv("EASY_SPEAK_PASSWORD") 
    }

    # Perform login
    login_response = scraper.post(login_url, data=login_payload)

    # Check if login was successful
    if login_response.status_code == 200:
        print("Login successful!")

    # Now fetch the agenda page
    agenda_url = "https://easy-speak.org/viewagenda.php?t=586027&pr=1"
    agenda_response = scraper.get(agenda_url)

    generate_pdf(agenda_response)

    get_screenshot()