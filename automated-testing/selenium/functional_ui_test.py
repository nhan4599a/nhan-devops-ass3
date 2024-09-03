# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging

# Start the browser and login with standard_user
def run_function_ui_automation_test(user, password):
    logging.basicConfig(
        filename='functional_ui_test_selenium.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    logging.info('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    # for debugging enable driver constructor with no options
    # driver = webdriver.Chrome()

    # Test Login to the site
    logging.info('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_css_selector("input[id='login-button']").click()

    path_content_div = "div[id='inventory_container']"
    results = driver.find_element_by_css_selector(f"{path_content_div} > div[class='header_secondary_container'] span[class='title']").text
    assert "Products" in results
    logging.info(f"Successfully logged in as {user}")

    total_products = '6'

    # Test Add Items to Shopping Cart
    logging.info("Starting the shopping...")
    path_inventory_item = f"{path_content_div} > div[id='inventory_container'] > div[class='inventory_list'] > div[class='inventory_item']"
    product_items = driver.find_elements_by_css_selector(path_inventory_item)
    assert len(product_items) == int(total_products)
    logging.info("Successfully found 6 product items.")
    
    for i in range(6):
        path_product_item_name = f"{path_inventory_item} > div[class='inventory_item_label'] > a[id='item_{i}_title_link'] > div[class='inventory_item_name']"
        product_item_name = driver.find_element_by_css_selector(path_product_item_name)
        product_item_name.find_element_by_xpath('..//..//..//div[@class="pricebar"]//button[@class="btn_primary btn_inventory"]').click()
        logging.info("Succesfully added to shopping cart: " + product_item_name.text)

    path_shopping_cart_url = "div[id='page_wrapper'] > div[id='contents_wrapper'] > div[id='header_container'] > div[id='shopping_cart_container'] > a.shopping_cart_link.fa-layers.fa-fw"
    path_shopping_cart_badge = f"{path_shopping_cart_url} > span.fa-layers-counter.shopping_cart_badge"
    shopping_cart_total_items = driver.find_element_by_css_selector(path_shopping_cart_badge).text
    assert total_products == shopping_cart_total_items
    logging.info(f'Succesfully added {total_products} items to shopping cart')

    # Test Remove Items from Shopping Cart
    logging.info("Destroying shopping cart...")
    driver.find_element_by_css_selector(path_shopping_cart_url).click()
    cart_title = driver.find_element_by_css_selector("div[id='contents_wrapper'] > div[class='subheader']").text
    assert 'Cart' in cart_title
    logging.info("Successfully visited the Shopping Cart page.")

    path_cart_item_remove_buttons = "div[id='cart_contents_container'] div[class='cart_list'] > div[class='cart_item'] div[class='item_pricebar'] button"
    remove_item_buttons = driver.find_elements_by_css_selector(path_cart_item_remove_buttons)
    
    for remove_button in remove_item_buttons:
        shopping_cart_item_name = remove_button.find_element_by_xpath('..//..//a[contains(@id, "_title_link")]//div[@class="inventory_item_name"]').text
        remove_button.click()
        logging.info(f'Succesfully removed a product with name "{shopping_cart_item_name}" from shopping cart')

    shopping_cart_total_items = driver.find_elements_by_css_selector(path_shopping_cart_badge)
    assert 0 == len(shopping_cart_total_items)
    logging.info("Succesfully removed all products from shopping cart.")


run_function_ui_automation_test('standard_user', 'secret_sauce')