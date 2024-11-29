import base64
import cloudscraper
import os
from dotenv import load_dotenv
import time
import random



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

def get_one_page_print_options() -> dict:
    print_options = {
                "paperWidth": 8.5,   # Width in inches (e.g., 8.5 for Letter size)
                "paperHeight": 11,   # Height in inches (e.g., 11 for Letter size)
                "scale": .72,        # Adjust the scale to fit content (smaller scale shrinks content)
                "marginTop": 0,      # Margins can also be minimized to fit more content
                "marginBottom": 0,
                "marginLeft": 0,
                "marginRight": 0,
            }

    return print_options
def get_agenda():
    # Path to the Chrome for Testing binary and ChromeDriver
    chrome_driver_path = "../chrome-for-testing/chromedriver-mac-arm64/chromedriver"
    chrome_binary_path = "../chrome-for-testing/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

    # Set up Selenium WebDriver with Chrome for Testing
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary_path  # Use the Chrome for Testing binary
    options.add_argument("--headless")
    # The following arguments are necessary to make sure easy speak doesn't think this app is trying to maliciously interact with the site.
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


    # Start WebDriver with Chrome for Testing driver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Define print options for one-page output
    print_options = get_one_page_print_options()
    try:
        # Navigate to the desired webpage
        url = "https://easy-speak.org/viewagenda.php?t=586027&pr=1"  # Replace with your target URL
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Wait for 2-5 seconds randomly

        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", print_options)["data"]

        # Decode the Base64 string and save it as a PDF
        with open("agenda.pdf", "wb") as pdf_file:
            pdf_file.write(base64.b64decode(pdf_base64))

        print("PDF saved as 'agenda.pdf'.")

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
    

    generate_agenda()

    post_agenda_to_slack()