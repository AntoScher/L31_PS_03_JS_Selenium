import redis
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List
from functools import wraps
import time

from logger import setup_logger

logger = setup_logger()

class CacheManager:
    """Менеджер кэширования с использованием Redis"""
    
    def __init__(self, host='localhost', port=6379, db=0, default_ttl=3600):
        """
        Инициализация менеджера кэша
        
        Args:
            host: Хост Redis сервера
            port: Порт Redis сервера
            db: Номер базы данных Redis
            default_ttl: Время жизни кэша по умолчанию (в секундах)
        """
        self.redis_client = redis.Redis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=False,  # Для поддержки pickle
            socket_connect_timeout=5,
            socket_timeout=5
        )
        self.default_ttl = default_ttl
        self._test_connection()
    
    def _test_connection(self):
        """Тестирование подключения к Redis"""
        try:
            self.redis_client.ping()
            logger.info("Redis connection established")
        except redis.ConnectionError:
            logger.warning("Redis connection failed, using in-memory cache")
            self.redis_client = None
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Генерация ключа кэша"""
        # Создаем строку из аргументов
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        # Хешируем для получения короткого ключа
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Получение значения из кэша
        
        Args:
            key: Ключ кэша
            
        Returns:
            Значение из кэша или None если не найдено
        """
        if not self.redis_client:
            return None
            
        try:
            data = self.redis_client.get(key)
            if data:
                # Пытаемся десериализовать как JSON
                try:
                    return json.loads(data.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Если не JSON, пробуем pickle
                    return pickle.loads(data)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Сохранение значения в кэш
        
        Args:
            key: Ключ кэша
            value: Значение для сохранения
            ttl: Время жизни в секундах (None для использования default_ttl)
            
        Returns:
            True если успешно сохранено, False в противном случае
        """
        if not self.redis_client:
            return False
            
        try:
            ttl = ttl or self.default_ttl
            
            # Пытаемся сериализовать как JSON
            try:
                data = json.dumps(value, ensure_ascii=False, default=str)
                self.redis_client.setex(key, ttl, data.encode('utf-8'))
            except (TypeError, ValueError):
                # Если не удается сериализовать как JSON, используем pickle
                data = pickle.dumps(value)
                self.redis_client.setex(key, ttl, data)
            
            logger.info(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Удаление значения из кэша
        
        Args:
            key: Ключ кэша
            
        Returns:
            True если успешно удалено, False в противном случае
        """
        if not self.redis_client:
            return False
            
        try:
            result = self.redis_client.delete(key)
            if result:
                logger.info(f"Cache deleted: {key}")
            return bool(result)
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Проверка существования ключа в кэше
        
        Args:
            key: Ключ кэша
            
        Returns:
            True если ключ существует, False в противном случае
        """
        if not self.redis_client:
            return False
            
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    def get_ttl(self, key: str) -> Optional[int]:
        """
        Получение оставшегося времени жизни ключа
        
        Args:
            key: Ключ кэша
            
        Returns:
            Оставшееся время жизни в секундах или None
        """
        if not self.redis_client:
            return None
            
        try:
            ttl = self.redis_client.ttl(key)
            return ttl if ttl > 0 else None
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return None
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Очистка кэша по паттерну
        
        Args:
            pattern: Паттерн для поиска ключей (например, "search:*")
            
        Returns:
            Количество удаленных ключей
        """
        if not self.redis_client:
            return 0
            
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Cache cleared pattern {pattern}: {deleted} keys deleted")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Error clearing cache pattern {pattern}: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Получение статистики кэша
        
        Returns:
            Словарь со статистикой
        """
        if not self.redis_client:
            return {"status": "disabled"}
            
        try:
            info = self.redis_client.info()
            return {
                "status": "connected",
                "total_keys": info.get('db0', {}).get('keys', 0),
                "memory_usage": info.get('used_memory_human', 'N/A'),
                "uptime": info.get('uptime_in_seconds', 0)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"status": "error", "error": str(e)}

def cache_result(prefix: str = "default", ttl: Optional[int] = None):
    """
    Декоратор для кэширования результатов функций
    
    Args:
        prefix: Префикс для ключей кэша
        ttl: Время жизни кэша в секундах
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем экземпляр менеджера кэша
            cache_manager = CacheManager()
            
            # Генерируем ключ кэша
            cache_key = cache_manager._generate_key(prefix, *args, **kwargs)
            
            # Пытаемся получить результат из кэша
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result
            
            # Выполняем функцию
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Сохраняем результат в кэш
            cache_manager.set(cache_key, result, ttl)
            logger.info(f"Cache miss for {func.__name__}: {cache_key} (execution time: {execution_time:.2f}s)")
            
            return result
        return wrapper
    return decorator

def cache_search_results(ttl: int = 3600):
    """Специализированный декоратор для кэширования результатов поиска"""
    return cache_result(prefix="search", ttl=ttl)

def cache_navigation_results(ttl: int = 1800):
    """Специализированный декоратор для кэширования результатов навигации"""
    return cache_result(prefix="navigation", ttl=ttl)

# Глобальный экземпляр менеджера кэша
cache_manager = CacheManager()
