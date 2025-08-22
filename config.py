import os
from typing import Dict, Any

class Config:
    """Конфигурация приложения"""
    
    # Настройки браузера
    BROWSER_TIMEOUT = 30
    IMPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    
    # Настройки Chrome
    CHROME_OPTIONS = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--window-size=1920,1080',
        '--disable-blink-features=AutomationControlled'
    ]
    
    # Настройки Wikipedia
    WIKIPEDIA_URL = "https://www.wikipedia.org/"
    SEARCH_TIMEOUT = 10
    NAVIGATION_DELAY = 3
    
    # Настройки логирования
    LOG_LEVEL = "INFO"
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Настройки пользовательского интерфейса
    MAX_PARAGRAPHS_DISPLAY = 10
    MAX_LINKS_DISPLAY = 20
    
    @classmethod
    def get_browser_options(cls) -> Dict[str, Any]:
        """Возвращает настройки браузера"""
        return {
            'timeout': cls.BROWSER_TIMEOUT,
            'implicit_wait': cls.IMPLICIT_WAIT,
            'page_load_timeout': cls.PAGE_LOAD_TIMEOUT,
            'chrome_options': cls.CHROME_OPTIONS
        }
    
    @classmethod
    def get_wikipedia_settings(cls) -> Dict[str, Any]:
        """Возвращает настройки Wikipedia"""
        return {
            'url': cls.WIKIPEDIA_URL,
            'search_timeout': cls.SEARCH_TIMEOUT,
            'navigation_delay': cls.NAVIGATION_DELAY
        }
