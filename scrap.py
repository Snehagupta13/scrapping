from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 30)

driver.get(
    "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm"
)

# ✅ Correct locator from your screenshot
review_panel_dropdown = wait.until(
    EC.presence_of_element_located((By.NAME, "panel"))
)

select = Select(review_panel_dropdown)

for option in select.options:
    value = option.get_attribute("value")
    text = option.text.strip()

    if not value:
        continue

    print(f"Searching Review Panel: {text}")

    # Re-locate dropdown
    review_panel_dropdown = wait.until(
        EC.presence_of_element_located((By.NAME, "panel"))
    )
    select = Select(review_panel_dropdown)
    select.select_by_value(value)

    # ✅ Correct Search button (FORM-BASED)
    search_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//select[@name='panel']/ancestor::form//input[@type='submit']")
        )
    )
    search_button.click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)

    driver.back()
    wait.until(EC.presence_of_element_located((By.NAME, "panel")))


driver.quit()
