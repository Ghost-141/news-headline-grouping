from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_chrome_driver(headless=True):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => false})"},
    )

    return driver


def wait_for_elements(driver, selector, by=By.CSS_SELECTOR, timeout=20):
    """
    Wait for elements to be present and return them.
    Returns an empty list if timeout occurs.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, selector))
        )
        return driver.find_elements(by, selector)
    except TimeoutException:
        return []

def get_element_text(element, selector, by=By.CSS_SELECTOR, default=""):
    """Safely extract text from an element"""
    try:
        el = element.find_element(by, selector)
        return el.text.strip()
    except:
        return default


def get_element_attribute(element, selector, attribute, by=By.CSS_SELECTOR, default=""):
    """Safely extract attribute from an element"""
    try:
        el = element.find_element(by, selector)
        return el.get_attribute(attribute) or default
    except:
        return default
