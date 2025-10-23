from tkinter import *
from tkinter import ttk, messagebox


class ListPage:
    def __init__(self, parent, app, user_name=None):
        self.parent = parent
        self.app = app

        self.selected_test = None
        self.user_name = user_name

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
                                     font=('Arial', 14),
                                     selectbackground='#6e6e6e',
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

        # Кнопка удаления теста
        self.DelBtn = ttk.Button(self.parent,
                                 text="Удалить тест",
                                 style='StyleRed.TButton',
                                 command=self.delete_test)
        self.DelBtn.pack(side=LEFT, pady=10, ipady=5)

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
        custom_tests = self.app.test_manager.get_custom_tests()

        self.tests_listbox.delete(0, END)

        for test_name in available_tests:
            if test_name not in custom_tests:
                self.tests_listbox.insert(END, test_name)

        if custom_tests:
            self.tests_listbox.insert(END, "─" * 50)

            for test_name in custom_tests:
                self.tests_listbox.insert(END, f"{test_name}")

    def on_test_select(self, event):
        """Выбор теста из списка"""
        selection = self.tests_listbox.curselection()
        if selection:
            self.selected_test = self.tests_listbox.get(selection[0])

            is_custom = self.selected_test in self.app.test_manager.get_custom_tests()

            self.StartBtn.config(state='normal')

            self.DelBtn.config(state='normal' if is_custom else 'disable')
        else:
            self.StartBtn.config(state='disable')
            self.DelBtn.config(state='disable')

    def start_test(self):
        """Запуск выбранного теста"""
        if self.selected_test:
            if self.selected_test == "─" * 50:  # Проверка, что выбранный тест, это не полоса разделения
                self.error_label.config(foreground='red')
                return
            from pages.test_page import TestPage  # Импортируем страницу теста
            self.app.show_page(TestPage, test_name=self.selected_test, user_name=self.user_name)
        else:
            self.error_label.config(foreground='red')

    def delete_test(self):
        if not self.selected_test:
            self.error_label.config(foreground='red')
            return

        if self.selected_test not in self.app.test_manager.get_custom_tests():
            messagebox.showwarning("Внимание", "Можно удалять только пользовательские тесты")
            return

        result = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить тест {self.selected_test}"
        )

        if result:
            success = self.app.test_manager.remove_custom_test(self.selected_test)
            if success:
                messagebox.showinfo("Успех", f"Тест '{self.selected_test}' успешно удален")
                self.selected_test = None
                self.load_tests_list()
                self.StartBtn.config(state='disable')
                self.DelBtn.config(state='disable')
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить тест")

    # Функция возвращения на экран главного меню
    def back_button(self):
        from pages.main_menu import MainMenu  # Импорт не в начале, т.к. иначе будет ошибка
        self.app.show_page(MainMenu)

    # Очистка виджетов при закрытии страницы
    def destroy(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
