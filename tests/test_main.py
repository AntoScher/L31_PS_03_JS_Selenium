import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import tempfile
import shutil

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
    
    def test_create_driver_failure(self):
        """Тест неудачного создания драйвера"""
        with patch('main.ChromeDriverManager') as mock_manager:
            mock_manager.side_effect = Exception("Driver installation failed")
            
            from main import create_driver
            driver = create_driver()
            
            self.assertIsNone(driver)
    
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
    
    def test_search_wikipedia_timeout(self):
        """Тест таймаута при поиске"""
        with patch('main.create_driver') as mock_create:
            with patch('main.WebDriverWait') as mock_wait:
                from selenium.common.exceptions import TimeoutException
                mock_create.return_value = self.mock_driver
                mock_wait.return_value.until.side_effect = TimeoutException("Timeout")
                
                from main import search_wikipedia
                result = search_wikipedia("test")
                
                self.assertIsNone(result)
    
    def test_search_wikipedia_driver_none(self):
        """Тест поиска с None драйвером"""
        with patch('main.create_driver') as mock_create:
            mock_create.return_value = None
            
            from main import search_wikipedia
            result = search_wikipedia("test")
            
            self.assertIsNone(result)
    
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
    
    def test_print_paragraphs_no_elements(self):
        """Тест вывода параграфов без элементов"""
        self.mock_driver.find_elements.return_value = []
        
        with patch('builtins.print') as mock_print:
            from main import print_paragraphs
            print_paragraphs(self.mock_driver)
            
            # Проверяем, что print был вызван для сообщения об отсутствии
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
    
    def test_print_links_no_elements(self):
        """Тест вывода ссылок без элементов"""
        self.mock_driver.find_elements.return_value = []
        
        with patch('builtins.print') as mock_print:
            from main import print_links
            print_links(self.mock_driver)
            
            # Проверяем, что print был вызван для сообщения об отсутствии
            self.assertTrue(mock_print.called)
    
    def test_print_contents(self):
        """Тест вывода содержимого"""
        with patch('main.print_paragraphs') as mock_paragraphs:
            with patch('main.print_links') as mock_links:
                from main import print_contents
                print_contents(self.mock_driver)
                
                mock_paragraphs.assert_called_once_with(self.mock_driver)
                mock_links.assert_called_once_with(self.mock_driver)
    
    def test_error_handling(self):
        """Тест обработки ошибок"""
        with patch('main.create_driver') as mock_create:
            mock_create.return_value = None
            
            from main import search_wikipedia
            result = search_wikipedia("test")
            
            self.assertIsNone(result)
    
    def test_main_function(self):
        """Тест основной функции main"""
        with patch('main.search_wikipedia') as mock_search:
            with patch('main.print_contents') as mock_print:
                with patch('builtins.input') as mock_input:
                    with patch('builtins.print') as mock_print_main:
                        mock_input.return_value = "quit"
                        mock_search.return_value = self.mock_driver
                        
                        from main import main
                        main()
                        
                        # Проверяем, что функции были вызваны
                        self.assertTrue(mock_print_main.called)

class TestDataManager(unittest.TestCase):
    """Тесты для DataManager"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.test_output_dir = tempfile.mkdtemp()
        with patch('os.path.exists') as mock_exists:
            with patch('os.makedirs') as mock_makedirs:
                mock_exists.return_value = False
                from data_manager import DataManager
                self.data_manager = DataManager(self.test_output_dir)
    
    def tearDown(self):
        """Очистка после каждого теста"""
        shutil.rmtree(self.test_output_dir, ignore_errors=True)
    
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
    
    def test_export_links_to_csv(self):
        """Тест экспорта ссылок в CSV"""
        with patch('builtins.open', create=True) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            links = [{"text": "Link 1", "url": "https://example.com/1"}]
            filename = self.data_manager.export_links_to_csv(links)
            
            self.assertIsNotNone(filename)
            mock_file.write.assert_called()
    
    def test_save_page_content(self):
        """Тест сохранения содержимого страницы"""
        with patch('builtins.open', create=True) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            title = "Test Page"
            content = {"paragraphs": ["Test"], "links": []}
            filename = self.data_manager.save_page_content(title, content)
            
            self.assertIsNotNone(filename)
            mock_file.write.assert_called()
    
    def test_get_search_statistics(self):
        """Тест получения статистики поиска"""
        with patch('os.listdir') as mock_listdir:
            mock_listdir.return_value = ["search_history_20240101_120000.json"]
            
            stats = self.data_manager.get_search_statistics()
            
            self.assertIsInstance(stats, dict)
            self.assertIn('total_searches', stats)

class TestCacheManager(unittest.TestCase):
    """Тесты для CacheManager"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        with patch('redis.Redis') as mock_redis:
            self.mock_redis = Mock()
            mock_redis.return_value = self.mock_redis
            self.mock_redis.ping.return_value = True
            
            from cache_manager import CacheManager
            self.cache_manager = CacheManager()
    
    def test_generate_key(self):
        """Тест генерации ключа кэша"""
        key = self.cache_manager._generate_key("test", "arg1", kwarg1="value1")
        self.assertIsInstance(key, str)
        self.assertGreater(len(key), 0)
    
    def test_get_cached_result(self):
        """Тест получения кэшированного результата"""
        self.mock_redis.get.return_value = b'{"result": "test"}'
        
        result = self.cache_manager.get("test_key")
        
        self.assertEqual(result, {"result": "test"})
        self.mock_redis.get.assert_called_once_with("test_key")
    
    def test_set_cached_result(self):
        """Тест установки кэшированного результата"""
        self.mock_redis.set.return_value = True
        
        result = self.cache_manager.set("test_key", {"result": "test"})
        
        self.assertTrue(result)
        self.mock_redis.set.assert_called_once()
    
    def test_delete_cached_result(self):
        """Тест удаления кэшированного результата"""
        self.mock_redis.delete.return_value = 1
        
        result = self.cache_manager.delete("test_key")
        
        self.assertTrue(result)
        self.mock_redis.delete.assert_called_once_with("test_key")
    
    def test_exists_cached_result(self):
        """Тест проверки существования кэшированного результата"""
        self.mock_redis.exists.return_value = 1
        
        result = self.cache_manager.exists("test_key")
        
        self.assertTrue(result)
        self.mock_redis.exists.assert_called_once_with("test_key")
    
    def test_get_ttl(self):
        """Тест получения TTL кэша"""
        self.mock_redis.ttl.return_value = 3600
        
        result = self.cache_manager.get_ttl("test_key")
        
        self.assertEqual(result, 3600)
        self.mock_redis.ttl.assert_called_once_with("test_key")
    
    def test_clear_pattern(self):
        """Тест очистки по паттерну"""
        self.mock_redis.keys.return_value = [b'test_key1', b'test_key2']
        self.mock_redis.delete.return_value = 2
        
        result = self.cache_manager.clear_pattern("test_*")
        
        self.assertEqual(result, 2)
        self.mock_redis.keys.assert_called_once_with("test_*")
    
    def test_get_stats(self):
        """Тест получения статистики кэша"""
        self.mock_redis.info.return_value = {"used_memory": 1024, "keyspace_hits": 100}
        
        stats = self.cache_manager.get_stats()
        
        self.assertIsInstance(stats, dict)
        self.mock_redis.info.assert_called_once()

class TestConfig(unittest.TestCase):
    """Тесты для Config"""
    
    def test_get_browser_options(self):
        """Тест получения опций браузера"""
        from config import Config
        
        options = Config.get_browser_options()
        
        self.assertIsInstance(options, dict)
        self.assertIn('timeout', options)
        self.assertIn('chrome_options', options)
    
    def test_get_wikipedia_settings(self):
        """Тест получения настроек Wikipedia"""
        from config import Config
        
        settings = Config.get_wikipedia_settings()
        
        self.assertIsInstance(settings, dict)
        self.assertIn('url', settings)
        self.assertIn('search_timeout', settings)

class TestLogger(unittest.TestCase):
    """Тесты для Logger"""
    
    def test_setup_logger(self):
        """Тест настройки логгера"""
        with patch('os.path.exists') as mock_exists:
            with patch('os.makedirs') as mock_makedirs:
                mock_exists.return_value = False
                
                from logger import setup_logger
                logger = setup_logger()
                
                self.assertIsNotNone(logger)
                mock_makedirs.assert_called_once_with('logs')
    
    def test_log_functions(self):
        """Тест функций логирования"""
        with patch('os.path.exists') as mock_exists:
            with patch('os.makedirs') as mock_makedirs:
                mock_exists.return_value = False
                
                from logger import setup_logger, log_search_query, log_navigation, log_error, log_performance
                
                logger = setup_logger()
                
                # Тестируем функции логирования
                log_search_query(logger, "test query")
                log_navigation(logger, "test action", "test details")
                log_error(logger, "test error", "test context")
                log_performance(logger, "test operation", 1.5)
                
                # Проверяем, что логгер работает
                self.assertIsNotNone(logger)

if __name__ == '__main__':
    unittest.main()
