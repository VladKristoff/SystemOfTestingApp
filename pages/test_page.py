from tkinter import *
from tkinter import ttk
from tests.tests import test1


class TestPage:
    def __init__(self, parent, app, test_name=None):
        self.parent = parent
        self.app = app
        self.test_name = test_name
        # Берём данные теста, если есть имя
        self.test_data = self.app.test_manager.get_tests(test_name) if test_name else None

        self.total_questions = len(self.test_data)
        self.seconds = 120  # Сколько времени даётся на тест
        self.count_questions = 1  # Переменная для подсчёта номера вопроса
        self.user_answers = []  # Для хранения ответов пользователя

        self.timer_running = True

        self.create_widgets()
        self.show_question()
        self.update_timer()

    def create_widgets(self):
        # Фрейм для верхних надписей
        self.top_frame = Frame(self.parent, background='white')
        self.top_frame.pack(fill=X, padx=10, pady=10)

        # Номер вопроса
        self.label_num = ttk.Label(self.top_frame,
                                   text=f'Вопрос {self.count_questions} из 10',
                                   font=('Arial', 16, 'bold'),
                                   style='Label.TLabel')
        self.label_num.pack(side='left', anchor='w', padx=20)

        # Таймер справа сверху
        self.label_timer = ttk.Label(self.top_frame,
                                     text=self.format_time(),
                                     font=('Cabin', 12),
                                     foreground='#4d4d4d',
                                     style='Label.TLabel')
        self.label_timer.pack(side='right', anchor='w')

        # Фрейм для тестов
        self.test_frame = Frame(self.parent,
                                relief=SOLID,
                                borderwidth=1,
                                background='white')
        self.test_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Текст вопроса
        self.question_label = ttk.Label(self.test_frame,
                                        text='',
                                        font=('Arial', 14, 'bold'),
                                        style='Label.TLabel',
                                        wraplength=800)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        # Фрейм для вариантов ответа
        self.answers_frame = Frame(self.test_frame,
                                   background='white')
        self.answers_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

        self.select_option = IntVar(value=-1)  # Для хранения выбранного ответа
        self.option_buttons = []

        # Кнопка "Назад к списку тестов"
        self.BackBtn = ttk.Button(self.parent,
                                  text='Назад к списку тестов',
                                  style='StyleGray.TButton',
                                  command=self.back_button)
        self.BackBtn.pack(side=LEFT, padx=20, pady=10, ipadx=5, ipady=5)

        # Кнопка "Следующий"
        self.NextBtn = ttk.Button(self.parent,
                                  text="Следующий",
                                  style='StyleGreen.TButton',
                                  command=self.next_question)
        self.NextBtn.pack(side='right', padx=20, pady=10, ipadx=5, ipady=5)

        # Надпись "Выберите вариант ответа"
        self.error_label = ttk.Label(self.parent,
                                     text='Выберите вариант ответа',
                                     foreground='white',
                                     font=('Arial', 12, 'bold'),
                                     style='Label.TLabel')
        self.error_label.pack(padx=20, pady=10, side=RIGHT)

    def show_question(self):
        questions_key = f"question_{self.count_questions}"
        if questions_key in self.test_data:
            questions_data = self.test_data[questions_key]

            # Отображение вопроса
            self.question_label.config(text=questions_data["question"])

            # Очищаем варианты ответа
            for widget in self.answers_frame.winfo_children():
                widget.destroy()
            self.option_buttons = []

            # Создание кнопок для вариантов ответа
            for i, option in enumerate(questions_data["options"]):
                rb = ttk.Radiobutton(self.answers_frame,
                                     text=str(option),
                                     variable=self.select_option,
                                     value=i,
                                     style='TRadiobutton')
                rb.pack(anchor='w', padx=20, pady=10)
                self.option_buttons.append(rb)

    # Функция перехода к следующему вопросу
    def next_question(self):
        # Сохраняем ответ пользователя
        if self.select_option.get() != -1:
            self.error_label.config(foreground='white')
            self.user_answers.append(self.select_option.get())
            # Выбор сбрасывается
            self.select_option.set(-1)

            self.count_questions += 1

            if self.count_questions > self.total_questions:
                self.finish_test()
            else:
                self.label_num.config(text=f'Вопрос {self.count_questions} из {self.total_questions}')

                if self.count_questions == self.total_questions:
                    self.NextBtn.configure(text='Завершить')
                self.show_question()
        else:
            self.error_label.config(foreground='red')

    # Функция завершения теста
    def finish_test(self):
        self.timer_running = False

    # Функция для возврата в главное меню
    def back_button(self):
        self.timer_running = False
        from pages.list_page import ListPage
        self.app.show_page(ListPage)

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
