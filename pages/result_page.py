from tkinter import *
from tkinter import ttk
import psycopg2


class ResultPage:
    def __init__(self, parent, app, time_complete=0, correct_answers=0, total_questions=0, user_name=None):
        self.parent = parent
        self.app = app

        self.time_complete = time_complete
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.user_name = user_name
        self.correct_percent = correct_answers / total_questions * 100

        self.create_widgets()
        self.label_grade_change()
        self.save_results_to_db()

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
                                            text=f"Правильных ответов: {self.correct_answers} из {self.total_questions} ({self.correct_percent}%)",
                                            font=('Arial', 15, 'bold'),
                                            style='Label.TLabel')
        self.label_true_answers.pack(pady=3)

        # Время прохождения
        self.label_travel_time = ttk.Label(self.body_frame,
                                           text=f"Время прохождения: {self.format_time()}",
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

    def label_grade_change(self):
        if self.correct_percent <= 30:
            self.label_grade.config(text="Результат: Плохо",
                                    foreground='red')
        elif self.correct_percent < 80:
            self.label_grade.config(text="Результат: Хорошо",
                                    foreground='#f0bc00')
        else:
            self.label_grade.config(text="Результат: Отлично",
                                    foreground='green')

    def format_time(self):
        self.minutes, self.secs = divmod(self.time_complete, 60)
        return f'{self.minutes:02d}:{self.secs:02d}'

    def save_results_to_db(self):
        try:
            conn = psycopg2.connect(dbname='ShumovVDBForTestApp',
                                    user='postgres',
                                    password='1234',
                                    host='localhost',
                                    port='5432')
            cursor = conn.cursor()
            # Сначала находим или создаем пользователя
            cursor.execute('SELECT id FROM users WHERE name = %s', (self.user_name,))
            user_result = cursor.fetchone()

            if user_result:
                user_id = user_result[0]
            else:
                # Создаем нового пользователя
                cursor.execute('INSERT INTO users (name) VALUES (%s) RETURNING id', (self.user_name,))
                user_id = cursor.fetchone()[0]

            # Вставляем результаты теста
            cursor.execute('''INSERT INTO test_info 
        (user_name, test_name, total_questions, correct_answers, percent_correct_answers, time_complete, user_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (self.user_name, 'Математический тест', self.total_questions, self.correct_answers,
                            self.correct_percent, self.time_complete, user_id))
            conn.commit()
            print("Результаты успешно сохранены")
            cursor.execute('SELECT * FROM test_info')
            print(cursor.fetchall())



        except psycopg2.Error as e:
            print(f'Ошибка подключения к базе данные: {e}')
