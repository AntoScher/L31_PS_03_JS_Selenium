from selenium import webdriver

print("Testing setup...")
try:
    driver = webdriver.Chrome()
    print("Chrome WebDriver initialized successfully!")
    driver.get("https://www.google.com")
    print("Navigated to Google successfully!")
    driver.quit()
    print("Test completed successfully!")
except Exception as e:
    print(f"Error: {str(e)}")