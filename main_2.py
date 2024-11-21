from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def search_wikipedia(query):
    driver = webdriver.Chrome()
    driver.get("https://www.wikipedia.org/")
    
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(3)
    
    return driver

def print_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for index, para in enumerate(paragraphs):
        print(f"Paragraph {index + 1}: {para.text}\n")
        
def print_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")
    for index, link in enumerate(links):
        print(f"Link {index + 1}: {link.text} - {link.get_attribute('href')}\n")

def print_contents(driver):
    """Выводит содержание (оглавление) статьи"""
    contents = driver.find_elements(By.CSS_SELECTOR, ".toc li")
    for index, item in enumerate(contents):
        print(f"{index + 1}. {item.text}")
    return contents

def go_to_section(driver, section_index):
    """Переходит к выбранному разделу статьи"""
    try:
        section = section_index.split('.')
        main_section = int(section[0]) - 1
        sub_section = int(section[1]) if len(section) > 1 else None

        contents = driver.find_elements(By.CSS_SELECTOR, ".toc li")
        link = contents[main_section].find_element(By.TAG_NAME, "a")
        
        if sub_section is not None:
            sub_contents = link.find_elements(By.XPATH, ".//following-sibling::ul//a")
            link = sub_contents[sub_section - 1]

        link.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error navigating to section: {e}")

def main():
    query = input("Enter the initial search query: ")
    driver = search_wikipedia(query)
    
    print("\nTable of Contents for the current article:")
    contents = print_contents(driver)
    
    section_choice = input("Enter the number of the section you want to go to (e.g., 1 or 2.1): ")
    go_to_section(driver, section_choice)
    
    while True:
        print("\nWhat would you like to do next?")
        print("1. Scroll through paragraphs of the current section")
        print("2. Go to one of the related pages")
        print("3. Exit the program")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        
        if choice == "1":
            print_paragraphs(driver)
        elif choice == "2":
            print_links(driver)
            link_choice = int(input("Enter the number of the link you want to follow: ")) - 1
            links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")
            links[link_choice].click()
            time.sleep(3)
            print("\nTable of Contents for the new article:")
            contents = print_contents(driver)
            section_choice = input("Enter the number of the section you want to go to (e.g., 1 or 2.1): ")
            go_to_section(driver, section_choice)
        elif choice == "3":
            driver.quit()
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()
