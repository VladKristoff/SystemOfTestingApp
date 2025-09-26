from tests.tests1 import test1, test2, test_python_basics, test_programming_concepts, test_web_basics


class TestManager:
    def __init__(self):
        self.tests = {}
        self.load_tests()
        self.custom_tests = {}

    def load_tests(self):
        """Загружает стандартные тесты"""
        self.tests["Математический тест"] = test1
        self.tests["Тест по пайтон"] = test_python_basics
        self.tests["Тест по алгоритмам"] = test_programming_concepts
        self.tests["Тест по HTML и CSS"] = test_web_basics
        self.tests["Короткий тест для тестирования"] = test2

    def add_custom_test(self, test_name, test_data):
        # Если тест с таким именем уже существует, добавляем номер
        origin_name = test_name
        counter = 1
        while test_name in self.custom_tests or test_name in self.tests:
            test_name = f"{origin_name} ({counter})"
            counter += 1

        self.custom_tests[test_name] = test_data
        return test_name

    def get_available_tests(self):
        """Возвращает список доступных тестов"""
        all_tests = list(self.tests.keys()) + list(self.custom_tests.keys())
        return all_tests

    def get_tests(self, test_name):
        # Возвращает тест по имени
        if test_name in self.tests:
            return self.tests.get(test_name)
        elif test_name in self.custom_tests:
            return self.custom_tests[test_name]
        return None

    def remove_custom_test(self, test_name):
        if test_name in self.custom_tests:
            del self.custom_tests[test_name]
            return True
        return False

    def get_custom_tests(self):
        return list(self.custom_tests.keys())

