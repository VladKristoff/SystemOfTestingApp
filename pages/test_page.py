from tkinter import *
from tkinter import ttk
from tests.test1 import test1

class TestPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.seconds = 120 #  Сколько времени даётся на тест
        self.count_questions = 1 # Переменная для подсчёта номера вопроса
        self.timer_running = True

        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        # Фрейм для верхних надписей
        self.top_frame = Frame(self.parent, background='#f0f0f0')
        self.top_frame.pack(fill=X, padx=10, pady=10)

        # Номер вопроса
        self.label_num = ttk.Label(self.top_frame,
                                   text=f'Вопрос {self.count_questions} из 10',
                                   font=('Calibri', 14, 'bold'),
                                   style='Label.TLabel')
        self.label_num.pack(side='left', anchor='w')

        # Таймер справа сверху
        self.label_timer = ttk.Label(self.top_frame,
                              text=self.format_time(),
                              font=('Arial', 12),
                              foreground='#4d4d4d',
                              style='Label.TLabel')
        self.label_timer.pack(side='right', anchor='w')

        # Фрейм для тестов
        self.test_frame = Frame(self.parent,
                                relief=SOLID,
                                borderwidth=1)
        self.test_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Кнопка "Назад к меню"
        self.BackBtn = ttk.Button(self.parent,
                                  text='Назад к меню',
                                  style='StyleGray.TButton',
                                  command=self.back_button)
        self.BackBtn.pack(side=LEFT, padx=10, pady=10, ipadx=5, ipady=5)

        # Кнопка "Следующий"
        self.NextBtn = ttk.Button(self.parent, 
                                  text="Следующий",
                                  style='StyleGreen.TButton',
                                  command=self.NextQuestion)
        self.NextBtn.pack(side='right', padx=10, pady=10, ipadx=5, ipady=5)

    # Функция перехода к следующему вопросу
    def NextQuestion(self):
        self.count_questions += 1
        if self.count_questions == 9:
            self.NextBtn.configure(text='Завершить')
            self.label_num.configure(text=f'Вопрос {self.count_questions} из 10')
        elif self.count_questions <= 10:
            self.label_num.configure(text=f'Вопрос {self.count_questions} из 10')

    # Функция для возврата в главное меню
    def back_button(self):
        self.timer_running = False
        from pages.main_menu import MainMenu
        self.app.show_page(MainMenu)

    # Форматирование времени
    def format_time(self):
        self.minutes, self.secs = divmod(self.seconds, 60)
        return f'Время {self.minutes:02d}:{self.secs:02d}'
    
    # Обновление таймера каждую секунду
    def update_timer(self):
        if not self.timer_running:
            return
        if self.seconds > 0:
            try:
                self.label_timer.config(text=self.format_time())
                self.seconds -= 1
                self.parent.after(1000, self.update_timer)
            except TclError:
                return
        else:
            try:
                self.label_timer.config(text='Время истекло')
            except TclError:
                return

    # Очистка виджетов при закрытии страницы
    def destroy(self):
        self.timer_running = False
        for widget in self.parent.winfo_children():
            widget.destroy()
