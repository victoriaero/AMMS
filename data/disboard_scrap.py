from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time

def get_page(i):
    try:
        # Set up the Firefox WebDriver
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

        url = f"https://disboard.org/servers/{i}?fl=pt-BR&sort=-member_count"
        print(f"Accessing URL: {url}")  # Debugging
        driver.get(url)

        # Wait for the page to load completely
        time.sleep(5)  # Adjust the sleep time if necessary

        # Find the div and get its HTML
        div_element = driver.find_element(By.CLASS_NAME, 'columns.is-multiline.listing')
        div_html = div_element.get_attribute('outerHTML')

        # Write the HTML to a file
        with open(f'page_{i}_content.html', 'w', encoding='utf-8') as file:
            file.write(div_html)
    
    except Exception as e:
        print(f"An error occurred on iteration {i}: {e}")

    # Close the driver after the loop
    driver.quit()

for i in range(47, 51):
    time.sleep(10)
    get_page(i)