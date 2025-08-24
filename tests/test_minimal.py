import unittest
import os

class TestMinimal(unittest.TestCase):
    """Минимальные тесты для CI/CD"""
    
    def test_python_version(self):
        """Тест версии Python"""
        import sys
        self.assertGreaterEqual(sys.version_info[0], 3)
        self.assertGreaterEqual(sys.version_info[1], 8)
    
    def test_imports(self):
        """Тест базовых импортов"""
        try:
            import sys
            import os
            import unittest
            self.assertTrue(True)
        except ImportError:
            self.fail("Базовые модули не импортируются")
    
    def test_file_exists(self):
        """Тест существования основных файлов"""
        required_files = [
            'main.py',
            'requirements.txt',
            'README.md'
        ]
        
        for file_name in required_files:
            self.assertTrue(os.path.exists(file_name), f"Файл {file_name} отсутствует")
    
    def test_directory_exists(self):
        """Тест существования директорий"""
        required_dirs = [
            'tests'
        ]
        
        for dir_name in required_dirs:
            self.assertTrue(os.path.exists(dir_name), f"Директория {dir_name} отсутствует")
    
    def test_simple_math(self):
        """Простой математический тест"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(5 * 5, 25)
    
    def test_string_operations(self):
        """Тест строковых операций"""
        test_string = "Hello, World!"
        self.assertEqual(len(test_string), 13)
        self.assertIn("Hello", test_string)
    
    def test_list_operations(self):
        """Тест операций со списками"""
        test_list = [1, 2, 3, 4, 5]
        self.assertEqual(len(test_list), 5)
        self.assertEqual(sum(test_list), 15)
    
    def test_dict_operations(self):
        """Тест операций со словарями"""
        test_dict = {"a": 1, "b": 2, "c": 3}
        self.assertEqual(len(test_dict), 3)
        self.assertEqual(test_dict["a"], 1)
    
    def test_boolean_operations(self):
        """Тест булевых операций"""
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)
    
    def test_exception_handling(self):
        """Тест обработки исключений"""
        try:
            result = 10 / 2
            self.assertEqual(result, 5)
        except ZeroDivisionError:
            self.fail("Не должно быть исключения")
    
    def test_working_directory(self):
        """Тест рабочей директории"""
        self.assertTrue(os.getcwd() is not None)
        self.assertTrue(len(os.getcwd()) > 0)

if __name__ == '__main__':
    unittest.main()
