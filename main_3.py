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
        print(f"Параграф {index + 1}: {para.text}\n")
        
def print_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")
    for index, link in enumerate(links):
        print(f"Ссылка {index + 1}: {link.text} - {link.get_attribute('href')}\n")

def print_contents(driver):
    """Выводит содержание (оглавление) статьи"""
    contents = driver.find_elements(By.CSS_SELECTOR, ".toc li")
    if not contents:
        print("Содержание для этой статьи отсутствует.")
    for index, item in enumerate(contents):
        print(f"{index + 1}. {item.text}")
    return contents

def go_to_section(driver, section_index):
    """Переходит к выбранному разделу статьи"""
    try:
        contents = driver.find_elements(By.CSS_SELECTOR, ".toc li")
        if not contents:
            print("Нет доступных разделов для перехода.")
            return
        
        section = section_index.split('.')
        main_section = int(section[0]) - 1
        sub_section = int(section[1]) if len(section) > 1 else None
        
        if main_section >= len(contents):
            print("Номер раздела вне диапазона.")
            return
        
        link = contents[main_section].find_element(By.TAG_NAME, "a")
        
        if sub_section is not None:
            sub_contents = link.find_elements(By.XPATH, ".//following-sibling::ul//a")
            if sub_section - 1 >= len(sub_contents):
                print("Номер подраздела вне диапазона.")
                return
            link = sub_contents[sub_section - 1]
        
        link.click()
        time.sleep(2)
    except Exception as e:
        print(f"Ошибка при переходе к разделу: {e}")

def main():
    query = input("Введите первоначальный поисковый запрос: ")
    driver = search_wikipedia(query)
    
    print("\nСодержание текущей статьи:")
    contents = print_contents(driver)
    
    if contents:
        section_choice = input("Введите номер раздела, к которому хотите перейти (например, 1 или 2.1): ")
        go_to_section(driver, section_choice)
    
    while True:
        print("\nЧто бы вы хотели сделать дальше?")
        print("1. Пролистать параграфы текущего раздела")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        
        choice = input("Введите ваш выбор (1, 2 или 3): ")
        
        if choice == "1":
            print_paragraphs(driver)
        elif choice == "2":
            print_links(driver)
            link_choice = input("Введите номер ссылки, по которой хотите перейти: ")
            if link_choice.isdigit():
                link_choice = int(link_choice) - 1
                links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")
                if link_choice < len(links):
                    links[link_choice].click()
                    time.sleep(3)
                    print("\nСодержание новой статьи:")
                    contents = print_contents(driver)
                    if contents:
                        section_choice = input("Введите номер раздела, к которому хотите перейти (например, 1 или 2.1): ")
                        go_to_section(driver, section_choice)
                else:
                    print("Номер ссылки вне диапазона.")
            else:
                print("Некорректный ввод. Пожалуйста, введите правильный номер.")
        elif choice == "3":
            driver.quit()
            print("Выход из программы...")
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")
            
if __name__ == "__main__":
    main()
