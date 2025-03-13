from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium WebDriver (Headless for GitHub Actions)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (No GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Binance P2P page
url = "https://p2p.binance.com/trade/all-payments/USDT?fiat=PKR"
driver.get(url)
time.sleep(5)  # Wait for page load

# Scrape advertiser names (Fix CSS Selector)
advertisers = driver.find_elements(By.CSS_SELECTOR, "a.bn-balink.text-primaryText")
advertisers = [ad.text.strip() for ad in advertisers[:10]]  # Get first 10

# Scrape prices (Fix CSS Selector)
prices = driver.find_elements(By.CSS_SELECTOR, "div.headline5")
prices = [p.text.strip() for p in prices[:10]]  # Get first 10

# Close the driver
driver.quit()

# Save to CSV (GitHub Actions compatible)
df = pd.DataFrame({"Advertiser": advertisers, "Price (PKR)": prices})
df.to_csv("binance_p2p_prices.csv", index=False, encoding="utf-8")

print("✅ Data successfully scraped and saved as CSV!")
