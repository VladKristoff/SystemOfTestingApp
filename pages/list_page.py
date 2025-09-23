from tkinter import *
from tkinter import ttk


class ListPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.selected_test = None

        self.create_widgets()
        self.load_tests_list()

    def create_widgets(self):
        # Очистка основного виджета, перед открытием новой страницы
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Заголовок слева сверху
        self.label_title = ttk.Label(self.parent,
                                     text="Выберите тестирование из списка",
                                     style='Label.TLabel',
                                     font=('Arial', 14, 'bold'), )
        self.label_title.pack(anchor='sw', padx=30, pady=10)

        # Фрейм для списка
        self.list_frame = Frame(self.parent,
                                background="white",
                                relief='solid',
                                borderwidth=2)
        self.list_frame.pack(fill=BOTH, padx=30, pady=30, expand=True)

        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # ListBox для отображения тестов
        self.tests_listbox = Listbox(self.list_frame,
                                     yscrollcommand=self.scrollbar.set,
                                     font=('Arial', 12),
                                     selectbackground='#e6f3ff',
                                     selectmode=SINGLE,
                                     borderwidth=0,
                                     highlightthickness=0)
        self.tests_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tests_listbox.bind('<<ListboxSelect>>', self.on_test_select)

        self.scrollbar.config(command=self.tests_listbox.yview)

        # Кнопка "Назад к меню"
        self.BackBtn = ttk.Button(self.parent,
                                  text="Назад к меню",
                                  style='StyleGray.TButton',
                                  command=self.back_button)
        self.BackBtn.pack(side=LEFT, padx=30, pady=10, ipady=5)

        # Кнопка "Начать тест"
        self.StartBtn = ttk.Button(self.parent,
                                   text="Начать тест",
                                   style='StyleGreen.TButton',
                                   command=self.start_test)
        self.StartBtn.pack(side=RIGHT, padx=30, pady=10, ipady=5)

        # Надпись "Выберите тест из списка"
        self.error_label = ttk.Label(self.parent,
                                     text='Выберите тест из списка',
                                     foreground='white',
                                     font=('Arial', 12, 'bold'),
                                     style='Label.TLabel')
        self.error_label.pack(padx=20, pady=10, side=RIGHT)

    # Загрузка списка тестов
    def load_tests_list(self):
        available_tests = self.app.test_manager.get_available_tests()

        self.tests_listbox.delete(0, END)
        for test_name in available_tests:
            self.tests_listbox.insert(END, test_name)

    def on_test_select(self, event):
        """Выбор теста из списка"""
        selection = self.tests_listbox.curselection()
        if selection:
            self.selected_test = self.tests_listbox.get(selection[0])
            self.StartBtn.config(state='normal')
        else:
            self.StartBtn.config(state='disable')

    def start_test(self):
        """Запуск выбранного теста"""
        if self.selected_test:
            from pages.test_page import TestPage  # Импортируем страницу теста
            self.app.show_page(TestPage, test_name=self.selected_test)
        else:
            self.error_label.config(foreground='red')

    # Функция возвращения на экран главного меню
    def back_button(self):
        from pages.main_menu import MainMenu  # Импорт не в начале, т.к. иначе будет ошибка
        self.app.show_page(MainMenu)

    # Очистка виджетов при закрытии страницы
    def destroy(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
