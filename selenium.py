import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def login_admin(driver):
    driver.get('https://demo.opencart.com/admin/')
    driver.find_element(By.ID, 'input-username').send_keys('demo')
    driver.find_element(By.ID, 'input-password').send_keys('demo')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)
    try:
        driver.find_element(By.CSS_SELECTOR, '.btn-close').click()
    except:
        pass


def create_category(driver):
    driver.find_element(By.ID, 'menu-catalog').click()
    driver.find_element(By.XPATH, "//a[contains(text(),'Categories')]").click()
    driver.find_element(By.CSS_SELECTOR, 'a[data-original-title="Add New"]').click()
    driver.find_element(By.ID, 'input-name1').send_keys('Devices')
    driver.find_element(By.ID, 'input-meta-title1').send_keys('Devices Meta')
    driver.find_element(By.CSS_SELECTOR, 'button[data-original-title="Save"]').click()
    time.sleep(2)


def add_products(driver):
    driver.find_element(By.ID, 'menu-catalog').click()
    driver.find_element(By.XPATH, "//a[contains(text(),'Products')]").click()
    products = [('Mouse 1', 'Wireless Mouse 1'), ('Mouse 2', 'Wireless Mouse 2'),
                ('Keyboard 1', 'Mechanical Keyboard 1'), ('Keyboard 2', 'Mechanical Keyboard 2')]
    for name, desc in products:
        driver.find_element(By.CSS_SELECTOR, 'a[data-original-title="Add New"]').click()
        driver.find_element(By.ID, 'input-name1').send_keys(name)
        driver.find_element(By.ID, 'input-meta-title1').send_keys(desc)
        driver.find_element(By.XPATH, "//a[contains(text(),'Data')]").click()
        driver.find_element(By.ID, 'input-model').send_keys('Model_' + name)
        driver.find_element(By.XPATH, "//a[contains(text(),'Links')]").click()
        driver.find_element(By.ID, 'input-category').send_keys('Devices')
        time.sleep(1)
        driver.find_element(By.ID, 'input-category').send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, 'button[data-original-title="Save"]').click()
        time.sleep(2)


def check_products_on_main(driver, expected_products):
    driver.get('https://demo.opencart.com/')
    for name in expected_products:
        search_box = driver.find_element(By.NAME, 'search')
        search_box.clear()
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        assert name in driver.page_source, f"{name} not found on main page"
        print(f"{name} is visible on main page ✅")


def delete_products(driver, products_to_delete):
    driver.get('https://demo.opencart.com/admin/')
    driver.find_element(By.ID, 'menu-catalog').click()
    driver.find_element(By.XPATH, "//a[contains(text(),'Products')]").click()
    for name in products_to_delete:
        search_box = driver.find_element(By.ID, 'input-name')
        search_box.clear()
        search_box.send_keys(name)
        driver.find_element(By.ID, 'button-filter').click()
        time.sleep(2)
        try:
            driver.find_element(By.NAME, 'selected[]').click()
            driver.find_element(By.CSS_SELECTOR, 'button[data-original-title="Delete"]').click()
            driver.switch_to.alert.accept()
            time.sleep(2)
            print(f"{name} deleted ✅")
        except:
            print(f"{name} not found or already deleted ⚠️")


def final_check(driver, present_products, absent_products):
    driver.get('https://demo.opencart.com/')
    for name in present_products:
        search_box = driver.find_element(By.NAME, 'search')
        search_box.clear()
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        assert name in driver.page_source, f"{name} should be present but not found"
        print(f"{name} is still visible ✅")

    for name in absent_products:
        search_box = driver.find_element(By.NAME, 'search')
        search_box.clear()
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        assert name not in driver.page_source, f"{name} should be deleted but still found"
        print(f"{name} is correctly removed ✅")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        login_admin(driver)
        create_category(driver)
        add_products(driver)
        check_products_on_main(driver, ['Mouse 1', 'Mouse 2', 'Keyboard 1', 'Keyboard 2'])
        delete_products(driver, ['Mouse 1', 'Keyboard 1'])
        final_check(driver, ['Mouse 2', 'Keyboard 2'], ['Mouse 1', 'Keyboard 1'])
    finally:
        driver.quit()
        print("Test completed and browser closed.")

if __name__ == "__main__":
    main()
