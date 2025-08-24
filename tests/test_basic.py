import unittest

class TestBasic(unittest.TestCase):
    """Базовые тесты без внешних зависимостей"""
    
    def test_python_works(self):
        """Тест что Python работает"""
        self.assertTrue(True)
        self.assertFalse(False)
    
    def test_math_works(self):
        """Тест математических операций"""
        self.assertEqual(1 + 1, 2)
        self.assertEqual(2 * 3, 6)
        self.assertEqual(10 / 2, 5)
    
    def test_strings_work(self):
        """Тест строковых операций"""
        text = "Hello World"
        self.assertEqual(len(text), 11)
        self.assertIn("Hello", text)
    
    def test_lists_work(self):
        """Тест списков"""
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(len(numbers), 5)
        self.assertEqual(sum(numbers), 15)
    
    def test_dicts_work(self):
        """Тест словарей"""
        data = {"name": "test", "value": 42}
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"], "test")
    
    def test_conditionals_work(self):
        """Тест условных операторов"""
        x = 5
        y = 10
        self.assertTrue(x < y)
        self.assertFalse(x > y)
    
    def test_loops_work(self):
        """Тест циклов"""
        result = 0
        for i in range(5):
            result += i
        self.assertEqual(result, 10)
    
    def test_functions_work(self):
        """Тест функций"""
        def add(a, b):
            return a + b
        
        self.assertEqual(add(2, 3), 5)
    
    def test_exceptions_work(self):
        """Тест исключений"""
        try:
            result = 10 / 2
            self.assertEqual(result, 5)
        except:
            self.fail("Не должно быть исключения")
    
    def test_assertions_work(self):
        """Тест утверждений"""
        self.assertIsNotNone("test")
        self.assertIsInstance("test", str)
        self.assertGreater(10, 5)

if __name__ == '__main__':
    unittest.main()
