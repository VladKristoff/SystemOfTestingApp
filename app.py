from tkinter import *
from tkinter import ttk
from pages.main_menu import MainMenu


class AppTest:
    def __init__(self, root):
        self.root = root
        self.root.title('Система тестирования')
        self.root.geometry('1000x650-300-100')
        self.root.resizable(height=False, width=False)

        self.icon = PhotoImage(file='media/ico.png')
        self.root.iconphoto(True, self.icon)

        self.is_dark_theme = False # Флаг текущей темы

        # Добавляю стили
        self.setup_styles()

        # Основной фрейм
        self.main_frame = Frame(root, background='white')
        self.main_frame.pack(fill=BOTH, expand=True)

        self.current_page = None

    ### СТИЛИ
    def setup_styles(self):
        # Стиль для lable-ов (сделал потому-что после применения тему фон у lable-ов стал темнее основного фона)
        self.style_for_label = ttk.Style()
        self.style_for_label.theme_use('clam')
        self.style_for_label.configure('Label.TLabel',
                                      background='white')
        
        # Стили для кнопок
        self.style  = ttk.Style()
        self.style.theme_use('clam')

        # Зелёная кнопка
        self.style.configure('StyleGreen.TButton', 
                             font=('Calibri', 16, 'bold'), 
                             background="#1DC200", 
                             borderwidth=0,
                             foreground='white')
        self.style.map('StyleGreen.TButton',
                       background=[('active', '#1DC200')])
        
        # Синяя кнопка
        self.style.configure('StyleBlue.TButton',
                              font=('Calibri', 16, 'bold'),
                              background="#0099FF",
                              borderwidth=0,
                              foreground='white')
        self.style.map('StyleBlue.TButton',
                       background=[('active', "#0099FF")])
        
        # Тёмно-синяя кнопка
        self.style.configure('StyleDarkBlue.TButton',
                              font=('Calibri', 16, 'bold'),
                              background="#003CC7",
                              borderwidth=0,
                              foreground='white')
        self.style.map('StyleDarkBlue.TButton',
                       background=[('active', '#003CC7')])
        
        # Красная кнопка
        self.style.configure('StyleRed.TButton',
                              font=('Calibri', 14, 'bold'),
                              background="#A80000",
                              borderwidth=0,
                              foreground='white')
        self.style.map('StyleRed.TButton',
                       background=[('active', '#A80000')])
        
        # Серая кнопка
        self.style.configure('StyleGray.TButton',
                              font=('Calibri', 14, 'bold'),
                              background="#4D4D4D",
                              borderwidth=0,
                              foreground='white')
        self.style.map('StyleGray.TButton',
                       background=[('active', '#4D4D4D')])
        
        # Желтая кнопка
        self.style.configure('StyleYellow.TButton',
                              font=('Calibri', 14, 'bold'),
                              background="#C57000",
                              borderwidth=0,
                              foreground='white')
        self.style.map('StyleYellow.TButton',
                       background=[('active', '#C57000')])
        
    ### МЕТОД ДЛЯ ПОКАЗА СТРАНИЦ
    def show_page(self, page_class, *args, **kwargs):
        # Удаление текущей страницы
        if self.current_page:
            self.current_page.destroy()

        # Добавление страницы
        self.current_page = page_class(self.main_frame, self, *args, **kwargs)