from typing import Any
import cloudscraper
import os
from dotenv import load_dotenv
from weasyprint import HTML

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By


def generate_pdf(html_response: Any, output_file:str = "agenda.pdf")-> None:
    # Convert HTML content to PDF
    HTML(string=html_response.text).write_pdf(output_file)

def get_screenshot():
    #Todo figure out how to use chrome for testing with selenium
    pass


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