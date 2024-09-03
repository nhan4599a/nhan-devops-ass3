from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import logging

# Start the browser and login with standard_user
def run_function_ui_automation_test(user, password):
    logging.basicConfig(
        filename='functional_ui_test_selenium.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    logging.info('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-pipe')
    
    driver = webdriver.Chrome(options=options)
    
    # for debugging enable driver constructor with no options
    # driver = webdriver.Chrome()

    # Test Login to the site
    logging.info('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    driver.find_element(By.CSS_SELECTOR, "input#user-name").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "input#password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input#login-button").click()

    xpath_header_text = '//*[@id="header_container"]/div[2]/span'
    home_page_title = driver.find_element(By.XPATH, xpath_header_text).text
    assert "Products" in home_page_title
    logging.info(f"Successfully logged in as {user}")

    total_products = '6'

    xpath_content_div = "//*[@id='inventory_container']"
    # Test Add Items to Shopping Cart
    logging.info("Starting the shopping...")
    path_inventory_item = f"{xpath_content_div}/div[@class='inventory_list']/div[@class='inventory_item']"
    product_items = driver.find_elements(By.XPATH, path_inventory_item)
    assert len(product_items) == int(total_products)
    logging.info("Successfully found 6 product items.")

    for product_item in product_items:
        product_item_name = product_item.find_element(By.XPATH, "./div[@class='inventory_item_description']/div[@class='inventory_item_label']/a/div")
        product_item_name.find_element(By.XPATH, "../../../div[@class='pricebar']/button").click()
        logging.info(f"Succesfully added product with name '{product_item_name.text}' to shopping cart")

    xpath_shopping_cart_badge = "//div[@id='header_container']//div[@id='shopping_cart_container']//span[@class='shopping_cart_badge']"
    shopping_cart_badge = driver.find_element(By.XPATH, xpath_shopping_cart_badge)
    shopping_cart_total_items = shopping_cart_badge.text
    assert total_products == shopping_cart_total_items
    logging.info(f'Succesfully added {total_products} items to shopping cart')

    # Test Remove Items from Shopping Cart
    logging.info("Destroying shopping cart...")
    shopping_cart_badge.find_element(By.XPATH, '..').click()

    cart_title = driver.find_element(By.XPATH, xpath_header_text).text
    assert 'Your Cart' in cart_title
    logging.info("Successfully visited the Shopping Cart page.")

    card_items = driver.find_elements(By.XPATH, "//div[@id='cart_contents_container']//div[@class='cart_item']")
    
    for cart_item in card_items:
        shopping_cart_item_name = cart_item.find_element(By.XPATH, '//a[contains(@id, "_title_link")]//div[@class="inventory_item_name"]').text
        cart_item.find_element(By.XPATH, '//div[@class="item_pricebar"]/button').click()
        logging.info(f'Succesfully removed a product with name "{shopping_cart_item_name}" from shopping cart')

    logging.info("Succesfully removed all products from shopping cart.")


run_function_ui_automation_test('standard_user', 'secret_sauce')