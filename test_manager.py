from tests.tests1 import test1, test2, test_python_basics, test_programming_concepts, test_web_basics


class TestManager:
    def __init__(self):
        self.tests = {}
        self.load_tests()

    def load_tests(self):
        """Загружает тесты"""
        self.tests["Математический тест"] = test1
        self.tests["Тест по пайтон"] = test_python_basics
        self.tests["Тест по алгоритмам"] = test_programming_concepts
        self.tests["Тест по HTML и CSS"] = test_web_basics
        self.tests["Короткий тест для тестирования"] = test2

    def get_available_tests(self):
        """Возвращает список доступных тестов"""
        return list(self.tests.keys())

    def get_tests(self, test_name):
        # Возвращает тест по имени
        return self.tests.get(test_name)


