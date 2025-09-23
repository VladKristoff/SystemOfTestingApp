from tkinter import *
from tkinter import ttk


class ResultPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        # Надпись "Результаты тестирования"
        self.label_title = ttk.Label(self.parent,
                                     text="Результаты тестирования",
                                     font=('Arial', 17, 'bold'),
                                     style='Label.TLabel')
        self.label_title.pack(anchor='w', padx=20, pady=10)

        # Фрейм для всего
        self.body_frame = Frame(self.parent,
                                relief=SOLID,
                                borderwidth=2,
                                background='white')
        self.body_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Оценка
        self.label_grade = ttk.Label(self.body_frame,
                                     text="Результат: ",
                                     font=('Arial', 15, 'bold'),
                                     style='Label.TLabel')
        self.label_grade.pack(pady=10)

        # Количество правильных вариантов ответа
        self.label_true_answers = ttk.Label(self.body_frame,
                                     text="Правильных ответов: ",
                                     font=('Arial', 15, 'bold'),
                                     style='Label.TLabel')
        self.label_true_answers.pack(pady=3)

        # Время прохождения
        self.label_travel_time = ttk.Label(self.body_frame,
                                     text="Время прохождения: ",
                                     font=('Arial', 14,),
                                     style='Label.TLabel')
        self.label_travel_time.pack(pady=3)

        # Надпись "Детальный результат"
        self.label_detail = ttk.Label(self.body_frame,
                                     text="Детальный результат: ",
                                     font=('Arial', 15, 'bold'),
                                     style='Label.TLabel')
        self.label_detail.pack(anchor='w', padx=10)

        # Фрейм для детального результата
        self.detail_frame = Frame(self.body_frame,
                                  relief=SOLID,
                                  borderwidth=1,
                                  background='white')
        self.detail_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)
        