#!/usr/bin/env python
# coding: utf-8

# In[17]:


import time  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Use WebDriver Manager to get the appropriate ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Target URL
URL = "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint"
driver.get(URL)

# Wait for product elements to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "styles_product-link__DXW_d"))
    )
except:
    print("Timeout: Product elements did not load in time.")

# Get the full page source after JavaScript execution
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")

# Extract product links
product_links = soup.find_all("a", class_="styles_product-link__DXW_d")

# List to store scraped data
scraped_reviews = []

# Loop through each product link
for product in product_links[:5]:  # Limiting to 5 products for testing
    try:
        product_url = "https://www.michaels.com" + product["href"]
        print(f"Scraping product: {product_url}")
        
        # Navigate to the product page
        driver.get(product_url)
        time.sleep(3)  # Allow some time for JS execution

        # Wait explicitly for reviews to load
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "bv-rnr__sc-16dr7i1-3"))
            )
        except:
            print(f"No reviews found for {product_url}")
            continue  # Skip to the next product

        # Get dynamically loaded HTML content
        product_html = driver.execute_script("return document.documentElement.outerHTML")
        product_soup = BeautifulSoup(product_html, "html.parser")

        # Extract reviews
        reviews = product_soup.find_all("div", class_="bv-rnr__sc-16dr7i1-3 iqhSue")

        if reviews:
            for review in reviews:
                review_text = review.get_text(strip=True)
                scraped_reviews.append({"Product URL": product_url, "Review": review_text})
        else:
            print(f"Reviews not found in the parsed HTML for {product_url}")

    except Exception as e:
        print(f"Error scraping {product_url}: {e}")

# Close the Selenium driver
driver.quit()

# Print scraped reviews
for i, review_data in enumerate(scraped_reviews):
    print(f"Review {i+1}: {review_data['Review']} (Source: {review_data['Product URL']})")


# In[ ]:




