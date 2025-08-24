import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch

class TestBasicFunctionality(unittest.TestCase):
    """Базовые тесты для проверки функциональности"""
    
    def test_config_import(self):
        """Тест импорта конфигурации"""
        try:
            from config import Config
            self.assertTrue(hasattr(Config, 'BROWSER_TIMEOUT'))
            self.assertTrue(hasattr(Config, 'WIKIPEDIA_URL'))
        except ImportError:
            self.fail("Не удалось импортировать config")
    
    def test_logger_import(self):
        """Тест импорта логгера"""
        try:
            from logger import setup_logger
            logger = setup_logger()
            self.assertIsNotNone(logger)
        except ImportError:
            self.fail("Не удалось импортировать logger")
    
    def test_data_manager_import(self):
        """Тест импорта data_manager"""
        try:
            from data_manager import DataManager
            dm = DataManager()
            self.assertIsNotNone(dm)
        except ImportError:
            self.fail("Не удалось импортировать data_manager")
    
    def test_cache_manager_import(self):
        """Тест импорта cache_manager"""
        try:
            from cache_manager import CacheManager
            cm = CacheManager()
            self.assertIsNotNone(cm)
        except ImportError:
            self.fail("Не удалось импортировать cache_manager")
    
    def test_main_import(self):
        """Тест импорта main"""
        try:
            from main import create_driver, search_wikipedia
            self.assertTrue(callable(create_driver))
            self.assertTrue(callable(search_wikipedia))
        except ImportError:
            self.fail("Не удалось импортировать main")
    
    def test_config_methods(self):
        """Тест методов конфигурации"""
        from config import Config
        
        options = Config.get_browser_options()
        self.assertIsInstance(options, dict)
        self.assertIn('timeout', options)
        
        settings = Config.get_wikipedia_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn('url', settings)
    
    def test_logger_functions(self):
        """Тест функций логгера"""
        from logger import setup_logger, log_search_query, log_navigation, log_error, log_performance
        
        logger = setup_logger()
        
        # Тестируем функции логирования
        log_search_query(logger, "test query")
        log_navigation(logger, "test action", "test details")
        log_error(logger, "test error", "test context")
        log_performance(logger, "test operation", 1.5)
        
        self.assertIsNotNone(logger)
    
    def test_data_manager_methods(self):
        """Тест методов data_manager"""
        from data_manager import DataManager
        
        dm = DataManager()
        
        # Тестируем методы
        query = "test query"
        results = [{"title": "Test", "url": "https://test.com"}]
        
        with patch('builtins.open', create=True) as mock_open:
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            filename = dm.save_search_history(query, results)
            self.assertIsNotNone(filename)
    
    def test_cache_manager_basic(self):
        """Тест базовых методов cache_manager"""
        from cache_manager import CacheManager
        
        with patch('redis.Redis') as mock_redis:
            mock_redis_instance = Mock()
            mock_redis.return_value = mock_redis_instance
            mock_redis_instance.ping.return_value = True
            
            cm = CacheManager()
            
            # Тестируем генерацию ключа
            key = cm._generate_key("test", "arg1", kwarg1="value1")
            self.assertIsInstance(key, str)
            self.assertGreater(len(key), 0)
    
    def test_main_functions_mocked(self):
        """Тест функций main с моками"""
        from main import create_driver, search_wikipedia
        
        # Тестируем create_driver с моком
        with patch('main.ChromeDriverManager') as mock_manager:
            with patch('main.webdriver.Chrome') as mock_chrome:
                mock_driver = Mock()
                mock_manager.return_value.install.return_value = '/path/to/chromedriver'
                mock_chrome.return_value = mock_driver
                
                driver = create_driver()
                self.assertIsNotNone(driver)
        
        # Тестируем search_wikipedia с моком
        with patch('main.create_driver') as mock_create:
            with patch('main.WebDriverWait') as mock_wait:
                mock_driver = Mock()
                mock_element = Mock()
                mock_create.return_value = mock_driver
                mock_wait.return_value.until.return_value = mock_element
                
                result = search_wikipedia("test")
                self.assertIsNotNone(result)
    
    def test_requirements_installed(self):
        """Тест установки зависимостей"""
        try:
            import selenium
            import flask
            import redis
            import pytest
            import flake8
            import bandit
            import safety
            self.assertTrue(True)  # Все зависимости установлены
        except ImportError as e:
            self.fail(f"Отсутствует зависимость: {e}")
    
    def test_file_structure(self):
        """Тест структуры файлов"""
        required_files = [
            'main.py',
            'config.py',
            'logger.py',
            'data_manager.py',
            'cache_manager.py',
            'api_server.py',
            'requirements.txt',
            'Dockerfile',
            'docker-compose.yml',
            'Makefile',
            'README.md',
            'CHANGELOG.md'
        ]
        
        for file_name in required_files:
            self.assertTrue(os.path.exists(file_name), f"Файл {file_name} отсутствует")
    
    def test_directories_exist(self):
        """Тест существования директорий"""
        required_dirs = [
            'tests',
            'docs'
        ]
        
        for dir_name in required_dirs:
            self.assertTrue(os.path.exists(dir_name), f"Директория {dir_name} отсутствует")

if __name__ == '__main__':
    unittest.main()
