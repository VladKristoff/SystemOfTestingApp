from tkinter import *
from tkinter import ttk
from pages.test_page import TestPage
from pages.result_page import ResultPage

class MainMenu():
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Очистка основного виджета, перед открытием новой страницы
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Заголовок слева-сверху
        self.label_title = ttk.Label(self.parent,
                                     text='Система тестирования знаний',
                                     font=('Arial', 14, 'bold'),
                                     foreground='#303030',
                                     style='Label.TLabel')
        self.label_title.pack(anchor='sw', padx=10, pady=10)

        # Фрейм для основного меню
        self.menu_frame = Frame(self.parent,
                                background="#f0f0f0",
                                relief='solid',
                                borderwidth=1)
        self.menu_frame.pack(anchor='center', fill='both', expand=True, padx=175, pady=140)

        # Надпись "Главное меню"
        self.label_menu = ttk.Label(self.menu_frame,
                                    text="Главное меню",
                                    font=('Arial', 12, 'bold'),
                                    foreground='#303030',
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
                                     foreground='#f0f0f0',
                                     style='Label.TLabel')
        self.label_error.pack(anchor='s')

        # Поле ввода текста для имени
        self.entry_name = ttk.Entry(self.menu_frame,
                                    width=30,
                                    font=('Arial', 11))
        self.entry_name.pack(anchor='s')

        # Фрейм для кнопок
        self.frame_for_buttons = Frame(self.menu_frame)
        self.frame_for_buttons.pack(anchor='center', fill='both', expand=True, padx=50, pady=50)
        # Создание колонок для выравнивания
        self.frame_for_buttons.grid_columnconfigure(0, weight=1)
        self.frame_for_buttons.grid_columnconfigure(1, weight=1)
        self.frame_for_buttons.grid_columnconfigure(2, weight=1)

        # Кнопка "Начать тест"
        self.StartBtn = ttk.Button(self.frame_for_buttons,
                                   text='Начать тест',
                                   style='StyleGreen.TButton',
                                   command=self.start_test)
        self.StartBtn.grid(row=0, column=0, ipadx=11, ipady=9, padx=15)

        # Кнопка "Загрузить тест"
        self.LoadBtn = ttk.Button(self.frame_for_buttons,
                                  text='Загрузить тест',
                                  style='StyleDarkBlue.TButton', )
        self.LoadBtn.grid(row=0, column=1, ipadx=11, ipady=9, padx=15)

        # Кнопка "Результаты"
        self.ResultsBtn = ttk.Button(self.frame_for_buttons,
                                     text='Результаты',
                                     style='StyleBlue.TButton',
                                     command=self.start_results)
        self.ResultsBtn.grid(row=0, column=2, ipadx=11, ipady=9, padx=15)

        # Надпись "доступно 10 вопросов"
        self.lable_avaiable = ttk.Label(self.menu_frame,
                                        text="Доступно 10 вопросов",
                                        font=('Arial', 12),
                                        foreground='#4d4d4d',
                                        style='Label.TLabel')
        self.lable_avaiable.pack(anchor='s')

    # Функция перехода к странице теста
    def start_test(self):
        self.user_name = self.entry_name.get()
        if self.user_name:
            # Меняю цвет теста с ошибкой на цвет фона, на случай, если цвет менялся не красный
            self.app.show_page(TestPage)
        else:
            # Меняется цвет текста с ошибкой на красный, если не ввёдено имя
            self.label_error.configure(foreground='red')

    def start_results(self):
        self.app.show_page(ResultPage)

    # Очистка виджетов при закрытии страницы
    def destroy(self):
        for widget in self.parent.winfo_children():
            widget.destroy()