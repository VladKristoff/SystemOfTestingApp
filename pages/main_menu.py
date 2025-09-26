import json
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pages.test_page import TestPage
from pages.table_page import TablePage
from pages.list_page import ListPage


class MainMenu():
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.user_name = None

        self.create_widgets()

    def create_widgets(self):
        # Очистка основного виджета, перед открытием новой страницы
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Заголовок слева-сверху
        self.label_title = ttk.Label(self.parent,
                                     text='Система тестирования знаний',
                                     font=('Arial', 17, 'bold'),
                                     style='Label.TLabel', )
        self.label_title.pack(anchor='sw', padx=20, pady=20)

        # Фрейм для основного меню
        self.menu_frame = Frame(self.parent,
                                background="white",
                                relief='solid',
                                borderwidth=2)
        self.menu_frame.pack(anchor='center', fill='both', expand=True, padx=150, pady=120)

        # Надпись "Главное меню"
        self.label_menu = ttk.Label(self.menu_frame,
                                    text="Главное меню",
                                    font=('Arial', 14, 'bold'),
                                    style='Label.TLabel')
        self.label_menu.pack(anchor='nw', padx=5, pady=5)

        # Надпись "Введите ваше имя"
        self.label_name = ttk.Label(self.menu_frame,
                                    text="Введите ваше имя:",
                                    font=('Arial', 12),
                                    foreground='#4d4d4d',
                                    style='Label.TLabel')
        self.label_name.pack(anchor='s', pady=20)

        # Надпись с ошибкой, если не введено имя (по умолочанию под цвет фона)
        self.label_error = ttk.Label(self.menu_frame,
                                     text='Заполните обязательное поле!',
                                     font=('Calibri', 10),
                                     foreground='white',
                                     style='Label.TLabel')
        self.label_error.pack(anchor='s')

        # Поле ввода текста для имени
        self.entry_name = ttk.Entry(self.menu_frame,
                                    width=30,
                                    font=('Arial', 11), )
        self.entry_name.pack(anchor='s')

        # Фрейм для кнопок
        self.frame_for_buttons = Frame(self.menu_frame, background='white')
        self.frame_for_buttons.pack(anchor='center', fill='both', expand=True, padx=50, pady=50)
        # Создание колонок для выравнивания
        self.frame_for_buttons.grid_columnconfigure(0, weight=1)
        self.frame_for_buttons.grid_columnconfigure(1, weight=1)
        self.frame_for_buttons.grid_columnconfigure(2, weight=1)

        # Кнопка "Начать тест"
        self.StartBtn = ttk.Button(self.frame_for_buttons,
                                   text="Список тестов",
                                   style='StyleGreen.TButton',
                                   command=self.start_list_page)
        self.StartBtn.grid(row=0, column=0, ipadx=20, ipady=9, padx=15)

        # Кнопка "Загрузить тест"
        self.LoadBtn = ttk.Button(self.frame_for_buttons,
                                  text='Загрузить тест',
                                  style='StyleDarkBlue.TButton',
                                  command=self.load_custom_test)
        self.LoadBtn.grid(row=0, column=1, ipadx=20, ipady=9, padx=15)

        # Кнопка "Результаты"
        self.ResultsBtn = ttk.Button(self.frame_for_buttons,
                                     text='Результаты',
                                     style='StyleBlue.TButton',
                                     command=self.start_results)
        self.ResultsBtn.grid(row=0, column=2, ipadx=20, ipady=9, padx=15)

    def start_list_page(self):
        self.user_name = self.entry_name.get()
        if self.user_name:
            self.app.show_page(ListPage, user_name=self.user_name)
        else:
            # Меняется цвет текста с ошибкой на красный, если не ввёдено имя
            self.label_error.configure(foreground='red')

    def start_results(self):
        self.app.show_page(TablePage)

    def load_custom_test(self):
        # Загрузка пользовательского теста
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл теста",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if not file_path:
                return

            # Читаем и проверяем файл
            with open(file_path, 'r', encoding='utf-8') as file:
                test_data = json.load(file)

            # Проверяем структуру теста
            if self.validate_test(test_data):
                # Получаем название теста из имени файла или из данных
                test_name = self.get_test_name(file_path, test_data)

                added_test_name = self.app.test_manager.add_custom_test(test_name, test_data)
                messagebox.showinfo("Успех", f"Тест {added_test_name} успешно загружен!")

            else:
                messagebox.showerror("Ошибка", "Неверный формат теста. Проверьте структуру JSON файла.")

        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Ошибка чтения JSON файла. Проверьте формат файла.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке теста: {str(e)}")

    def validate_test(self, test_data):
        # Проверяем структуру загружаемого теста
        if not isinstance(test_data, dict):
            return False

        # Проверка наличия хотя бы одного вопроса
        has_questions = False
        for key, value in test_data.items():
            if key.startswith('question_'):
                if not all(k in value for k in ['question', 'options', 'correct_answer']):
                    return False
                if not isinstance(value['options'], list) or len(value['options']) == 0:
                    return False
                if not isinstance(value['correct_answer'], int):
                    return False
                has_questions = True

        return has_questions

    def get_test_name(self, file_path, test_data):
        # Пробуем получить название теста из имени файла
        if 'test_name' in test_data:
            return test_data['test_name']

        # Или используем имя файла без расширения
        import os
        file_name = os.path.basename(file_path)
        test_name = os.path.splitext(file_name)[0]
        return test_name

    # Очистка виджетов при закрытии страницы
    def destroy(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
