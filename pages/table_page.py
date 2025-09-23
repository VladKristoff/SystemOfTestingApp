from tkinter import *
from tkinter import ttk

class TablePage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        # Фрейм для верхних виджетов
        self.top_frame = Frame(self.parent, background='white')
        self.top_frame.pack(fill=X)

        # Надпись "Результаты ваших тестирований"
        self.label_YourResults = ttk.Label(self.top_frame,
                                           text='История результатов',
                                           font=('Arial', 14, 'bold'),
                                           style='Label.TLabel')
        self.label_YourResults.pack(side='left', padx=30, pady=10)

        # Фрейм для таблицы
        self.table_frame = Frame(self.parent,
                                 background='white',
                                 relief=SOLID,
                                 borderwidth=2)
        self.table_frame.pack(fill='both', expand=TRUE, padx=30, pady=30)

        # Кнопка "Назад", переход на главное меню
        self.BackBtn = ttk.Button(self.parent,
                                  text='Назад',
                                  style='StyleGray.TButton',
                                  command=self.back_button)
        self.BackBtn.pack(side='left', anchor='s', padx=30, pady=10, ipady=5)

        # Кнопка "Удалить"
        self.DelBtn = ttk.Button(self.parent,
                                  text='Удалить',
                                  style='StyleRed.TButton')
        self.DelBtn.pack(side='right', anchor='s', padx=30, pady=10, ipadx=5, ipady=5)

        # Кнопка "Очистить всё"
        self.ClearBtn = ttk.Button(self.parent,
                                  text='Очистить всё',
                                  style='StyleYellow.TButton')
        self.ClearBtn.pack(side='right', anchor='s', padx=10, pady=10, ipadx=5, ipady=5)

    # Функция возвращения на экран главного меню
    def back_button(self):
        from pages.main_menu import MainMenu # Импорт не в начале, т.к. иначе будет ошибка
        self.app.show_page(MainMenu)

    # Очистка виджетов при закрытии страницы
    def destroy(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

