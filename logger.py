import logging
import os
from datetime import datetime

def setup_logger():
    """Настройка системы логирования"""
    # Создаем папку для логов если её нет
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Настраиваем формат логов
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Создаем логгер
    logger = logging.getLogger('wikipedia_navigator')
    logger.setLevel(logging.INFO)
    
    # Создаем файловый обработчик
    log_filename = f'logs/wikipedia_navigator_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Создаем консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Создаем форматтер
    formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_search_query(logger, query):
    """Логирует поисковые запросы"""
    logger.info(f"Поисковый запрос: {query}")

def log_navigation(logger, action, details=""):
    """Логирует действия навигации"""
    logger.info(f"Навигация: {action} {details}")

def log_error(logger, error, context=""):
    """Логирует ошибки"""
    logger.error(f"Ошибка {context}: {error}")

def log_performance(logger, operation, duration):
    """Логирует производительность операций"""
    logger.info(f"Производительность {operation}: {duration:.2f} сек")
