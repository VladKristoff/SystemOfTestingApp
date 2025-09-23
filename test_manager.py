from tests.tests import test1, test2


class TestManager:
    def __init__(self):
        self.tests = {}
        self.load_tests()

    def load_tests(self):
        """Загружает тесты"""
        self.tests["Математический тест"] = test1
        self.tests["Математический тест 2"] = test2
        print(self.tests)

    def get_available_tests(self):
        """Возвращает список доступных тестов"""
        return list(self.tests.keys())

    def get_tests(self, test_name):
        # Возвращает тест по имени
        return self.tests.get(test_name)


