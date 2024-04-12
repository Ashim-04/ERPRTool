import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8050/")
    yield driver
    driver.quit()


def test_chart_selection(driver):
    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'chart-selector')))
    dropdown.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".Select-menu-outer")))

    # This assumes there's an element that changes when an option is selected.
    # The script will wait until this element is visible, indicating that the user has made a selection.
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'react-select-11--value-item')))


def test_dynamic_chart_updates(driver):
    # Click on the column selector to trigger the chart update.
    column_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'column-selector')))
    column_selector.click()
    # Choose a column. In absence of specific IDs for options
    first_column_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox'][1]")))
    first_column_option.click()



def test_uncheck_all_button(driver):
    uncheck_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'uncheck-all-button')))
    uncheck_button.click()
    WebDriverWait(driver, 10).until(lambda d: all(not checkbox.is_selected() for checkbox in d.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")))
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    assert all(not checkbox.is_selected() for checkbox in checkboxes)
