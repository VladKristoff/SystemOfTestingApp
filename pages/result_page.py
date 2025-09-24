from tkinter import *
from tkinter import ttk
import psycopg2


class ResultPage:
    def __init__(self, parent, app, time_complete=0, correct_answers=0, total_questions=0, user_name=None, test_name=None, user_answers=None):
        self.parent = parent
        self.app = app

        self.user_answers = user_answers
        self.time_complete = time_complete
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.user_name = user_name
        self.correct_percent = correct_answers / total_questions * 100
        # Берём данные теста, если есть имя
        self.test_data = self.app.test_manager.get_tests(test_name) if test_name else None

        self.create_widgets()
        self.label_grade_change()
        self.save_results_to_db()
        self.show_detail_info()

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

        # Canvas and scrollbar для прокрутки
        self.canvas = Canvas(self.detail_frame,
                              background="white",
                              highlightthickness=0)
        self.scrollbar = Scrollbar(self.detail_frame,
                                   orient='vertical',
                                   command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas,
                                    background='white')
        
        self.scrollable_frame.bind('<Configure>',
                                   lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Упаковываем scrollbar и canvas
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

    def show_detail_info(self):
        if not self.test_data or not self.user_answers:
            no_data_label = ttk.Label(self.scrollable_frame,
                                text="Детальная информация недоступна",
                                font=('Arial', 12),
                                background='white')
            no_data_label.pack(pady=20)
            return
        
        # Устанавливаем минимальную ширину для scrollable_frame
        self.scrollable_frame.update_idletasks()  # Обновляем геометрию
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 100:  # Если canvas еще не отрисовался
            canvas_width = 800  # Устанавливаем разумную ширину по умолчанию
    
        # Настраиваем scrollable_frame на всю ширину canvas
        self.canvas.itemconfig(self.canvas.find_all()[0], width=canvas_width)
        
        for count_questions in range(self.total_questions):
            questions_key = f"question_{count_questions+1}"
            if questions_key in self.test_data:
                questions_data = self.test_data[questions_key]
                user_answer_index = self.user_answers[count_questions] if count_questions < len(self.user_answers) else -1
                correct_answer_index = questions_data["correct_answer"]
                
                # Определяем, правильный ли ответ
                is_correct = user_answer_index == correct_answer_index

                # Создание фрейма для вопроса
                question_frame = Frame(self.scrollable_frame,
                                       background='#D7D7D7',
                                       relief=SOLID,
                                       borderwidth=1,
                                       width=800)
                question_frame.pack(fill=X, expand=True, padx=5, pady=5, ipady=10)
                question_frame.bind('<MouseWheel>', self._on_mousewheel)

                # Заголовок вопроса
                question_label = ttk.Label(question_frame,
                                           text=f"Вопрос {count_questions+1}: {questions_data['question']}",
                                           font=('Arial', 14, 'bold'),
                                           background='#D7D7D7',
                                           wraplength=800,
                                           justify=LEFT)
                question_label.pack(anchor='w', padx=10, pady=10)
                question_label.bind('<MouseWheel>', self._on_mousewheel)

                # Правильный ответ
                correct_answer_text = questions_data['options'][correct_answer_index]

                correct_label = ttk.Label(question_frame,
                                          text=f'Правильный ответ: {correct_answer_text}',
                                          font=('Cabin', 12),
                                          background="#D7D7D7",
                                          foreground="#444444",
                                          wraplength=800,
                                          justify=LEFT)
                correct_label.pack(anchor='w', padx=10)
                correct_label.bind('<MouseWheel>', self._on_mousewheel)

                # Ответ пользователя
                if user_answer_index != -1:
                    user_answer_text = questions_data['options'][user_answer_index]

                    user_label = Label(question_frame,
                                      text=f"Ваш ответ: {user_answer_text}",
                                      font=('Cabin', 12),
                                      background='#D7D7D7',
                                      foreground="#444444",
                                      justify=LEFT)
                    user_label.pack(anchor='w', padx=10)
                    user_label.bind('<MouseWheel>', self._on_mousewheel)

                else:
                    user_label = Label(question_frame,
                                      text="Ваш ответ: Не отвечено",
                                      font=('Arial', 11),
                                      background='#D7D7D7',
                                      foreground='red',
                                      justify=LEFT)
                    user_label.pack(anchor='w', padx=10, pady=2)
                    user_label.bind('<MouseWheel>', self._on_mousewheel)

                # Статус Правильно\Неправильно
                status_text = "✓ Правильно" if is_correct else "✗ Неправильно"
                status_color = 'green' if is_correct else 'red'

                status_label = ttk.Label(question_frame,
                                         text=status_text,
                                         foreground=status_color,
                                         font=('Arial', 13, 'bold'),
                                         background='#D7D7D7')
                status_label.pack(anchor='w', padx=10, pady=2)

        # Привязываем прокрутку к основным контейнерам
        self.scrollable_frame.bind('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)

        # Обновляем область прокрутки
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_mousewheel(self, event: Event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')


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
