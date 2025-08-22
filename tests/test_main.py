import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestWikipediaNavigator(unittest.TestCase):
    """Тесты для Wikipedia Navigator"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_driver = Mock()
        self.mock_element = Mock()
        self.mock_elements = [Mock(), Mock(), Mock()]
    
    def test_create_driver_success(self):
        """Тест успешного создания драйвера"""
        with patch('main.ChromeDriverManager') as mock_manager:
            with patch('main.webdriver.Chrome') as mock_chrome:
                mock_manager.return_value.install.return_value = '/path/to/chromedriver'
                mock_chrome.return_value = self.mock_driver
                
                from main import create_driver
                driver = create_driver()
                
                self.assertIsNotNone(driver)
                mock_chrome.assert_called_once()
    
    def test_search_wikipedia_success(self):
        """Тест успешного поиска в Wikipedia"""
        with patch('main.create_driver') as mock_create:
            with patch('main.WebDriverWait') as mock_wait:
                mock_create.return_value = self.mock_driver
                mock_wait.return_value.until.return_value = self.mock_element
                
                from main import search_wikipedia
                driver = search_wikipedia("Python programming")
                
                self.assertIsNotNone(driver)
                self.mock_driver.get.assert_called_once_with("https://www.wikipedia.org/")
    
    def test_print_paragraphs(self):
        """Тест вывода параграфов"""
        # Настройка моков
        self.mock_elements[0].text = "Первый параграф"
        self.mock_elements[1].text = "Второй параграф"
        self.mock_driver.find_elements.return_value = self.mock_elements
        
        with patch('builtins.print') as mock_print:
            from main import print_paragraphs
            print_paragraphs(self.mock_driver)
            
            # Проверяем, что print был вызван
            self.assertTrue(mock_print.called)
    
    def test_print_links(self):
        """Тест вывода ссылок"""
        # Настройка моков для ссылок
        link1 = Mock()
        link1.text = "Ссылка 1"
        link1.get_attribute.return_value = "https://example.com/1"
        
        link2 = Mock()
        link2.text = "Ссылка 2"
        link2.get_attribute.return_value = "https://example.com/2"
        
        self.mock_driver.find_elements.return_value = [link1, link2]
        
        with patch('builtins.print') as mock_print:
            from main import print_links
            print_links(self.mock_driver)
            
            # Проверяем, что print был вызван
            self.assertTrue(mock_print.called)
    
    def test_error_handling(self):
        """Тест обработки ошибок"""
        with patch('main.create_driver') as mock_create:
            mock_create.return_value = None
            
            from main import search_wikipedia
            result = search_wikipedia("test")
            
            self.assertIsNone(result)

class TestDataManager(unittest.TestCase):
    """Тесты для DataManager"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        with patch('os.path.exists') as mock_exists:
            with patch('os.makedirs') as mock_makedirs:
                mock_exists.return_value = False
                from data_manager import DataManager
                self.data_manager = DataManager("test_output")
    
    def test_save_search_history(self):
        """Тест сохранения истории поиска"""
        with patch('builtins.open', create=True) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            query = "test query"
            results = [{"title": "Test", "url": "https://test.com"}]
            
            filename = self.data_manager.save_search_history(query, results)
            
            self.assertIsNotNone(filename)
            mock_file.write.assert_called()
    
    def test_export_paragraphs_to_csv(self):
        """Тест экспорта параграфов в CSV"""
        with patch('builtins.open', create=True) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            paragraphs = ["Параграф 1", "Параграф 2"]
            filename = self.data_manager.export_paragraphs_to_csv(paragraphs)
            
            self.assertIsNotNone(filename)
            mock_file.write.assert_called()

if __name__ == '__main__':
    unittest.main()
