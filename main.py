# Импорт библиотек и классов
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QCalendarWidget
from PyQt5 import uic
import random
import sqlite3
import webbrowser
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QIcon, QIntValidator
from PyQt5.QtCore import QSize
from Calculator import Calculator
from Notepad import Notepad
from Photoshop import Photoshop
from Paint import Paint


# Календарь
class Calendar(QCalendarWidget):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        self.setWindowIcon(QIcon('icons/calendar.png'))
        self.setWindowTitle('Календарь')


# Рандомайзер
class Randomnum(QWidget):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        # Настройка окна
        self.setWindowTitle('Генератор рандомных чисел') # Задаём название окна
        self.setGeometry(500, 500, 500, 200) # Задаём размеры окна
        self.setWindowIcon(QIcon('icons/random.png')) # Задаём логотип окна
        self.setStyleSheet('background-color: white; color: black') # Настройка стилей
        # Создание лайаутов
        self.layout = QHBoxLayout()
        self.layout2 = QVBoxLayout()
        # Создание других виджетов и их настройка
        self.btn = QPushButton('Получить', self)
        self.btn.setStyleSheet('background-color: black; color: white')
        self.btn.clicked.connect(self.rand)
        self.label_info = QLabel(self)
        self.label_info.setFont(QFont('Arial', 20))
        self.label_info.setText('Выберите диапазон:')
        self.label_res = QLabel(self)
        self.label_res.setFont(QFont('Arial', 8))
        self.label_res.setText('')
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)
        self.input1.setValidator(QIntValidator())
        self.input2.setValidator(QIntValidator())
        # Добавление виджетов в лайауты и применение лайаута 2
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.input2)
        self.layout2.addWidget(self.label_info)
        self.layout2.addLayout(self.layout)
        self.layout2.addWidget(self.btn)
        self.layout2.addWidget(self.label_res)
        self.setLayout(self.layout2)

    def rand(self) -> None:
        # При корректно введённом промежутке
        try:
            self.label_res.setText(str(random.randint(int(self.input1.text()), int(self.input2.text())))) # Вывод числа
        # При некорректно введённом промежутке
        except ValueError:
            self.label_res.setText('Введены некорректные данные')


class WindowsProgram(QMainWindow):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        uic.loadUi('ui/WindowsXXL.ui', self) # Загрузка файла с дизайнера
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        # Настройка виджетов и окна
        self.setWindowTitle(('Windows Lite'))
        self.setWindowIcon(QIcon('icons/windows.jpg'))
        self.pushButton_calc.setIcon(QIcon('icons/calcul.png'))
        self.pushButton_calc.setIconSize(QSize(100, 100))
        self.pushButton_note.setIcon(QIcon('icons/notepad.jpg'))
        self.pushButton_note.setIconSize(QSize(100, 100))
        self.pushButton_yandex.setIcon(QIcon('icons/yandex.png'))
        self.pushButton_yandex.setIconSize(QSize(100, 100))
        self.pushButton_random.setIcon(QIcon('icons/random.png'))
        self.pushButton_random.setIconSize(QSize(100, 100))
        self.pushButton_calendar.setIcon(QIcon('icons/calendar.png'))
        self.pushButton_calendar.setIconSize(QSize(100, 100))
        self.pushButton_photoshop.setIcon(QIcon('icons/photoshop.png'))
        self.pushButton_photoshop.setIconSize(QSize(100, 100))
        self.pushButton_paint.setIcon(QIcon('icons/paint.png'))
        self.pushButton_paint.setIconSize(QSize(100, 100))
        self.setFixedSize(1280, 720)
        self.pushButton_hide.hide()
        self.radioButton_dark.hide()
        self.radioButton_light.hide()
        self.label.hide()
        # Связи виджетов с функциями
        self.pushButton_theme.clicked.connect(self.systembutton)
        self.pushButton_hide.clicked.connect(self.systembuttonhide)
        self.radioButton_dark.toggled.connect(self.changebg)
        self.radioButton_light.toggled.connect(self.changebg)
        self.pushButton_random.clicked.connect(self.random)
        self.pushButton_calc.clicked.connect(self.calc)
        self.pushButton_note.clicked.connect(self.notepad)
        self.pushButton_calendar.clicked.connect(self.calendar)
        self.pushButton_photoshop.clicked.connect(self.photoshop)
        self.pushButton_yandex.clicked.connect(lambda: webbrowser.open('https://yandex.ru/'))
        self.pushButton_paint.clicked.connect(self.paint)

    def systembutton(self) -> None: # Функция, срабатывающая при нажатии на кнопку: "Windows"
        self.pushButton_theme.setEnabled(False) # Отключение возможности нажимать на кнопку
        self.pushButton_hide.show()
        self.radioButton_dark.show()
        self.radioButton_light.show()
        self.label.show()

    def systembuttonhide(self) -> None: # Функция, срабатывающая при нажатии на кнопку: "Hide"
        self.pushButton_theme.setEnabled(True) # Включение возможности нажимать на кнопку
        self.pushButton_hide.hide()
        self.radioButton_dark.hide()
        self.radioButton_light.hide()
        self.label.hide()

    def changebg(self) -> None: # Функция, срабатывающая при изменении значения radioButton
        if self.sender().isChecked:
            if self.sender() == self.radioButton_light: # Если была нажата кнопка с надписью "Light"
                self.light_bg()
            elif self.sender() == self.radioButton_dark: # Если была нажата кнопка с надписью "Dark"
                self.dark_bg()

    def light_bg(self) -> None: # Изменение темы на светлую
        con = sqlite3.connect('dbs/buttons.db') # Обращение к БД
        self.centralWidget().setStyleSheet("background-color: white; color: #222222") # Изменение цвета фона и текста
        response = con.execute('''SELECT Button FROM Buttons''') # Получение данных из БД
        for elem in response: # Проход по данным из БД
            eval(elem[0]).setStyleSheet('QPushButton {background-color: #222222; color: white}') # Изменение стилей
        con.close()

    def dark_bg(self) -> None: # Изменение темы на тёмную
        con = sqlite3.connect('dbs/buttons.db') # Обращение к БД
        self.centralWidget().setStyleSheet(f"background-color: #222222; color: white") # Изменение цвета фона и текста
        response = con.execute('''SELECT Button FROM Buttons''') # Получение данных из БД
        for elem in response: # Проход по данным из БД
            eval(elem[0]).setStyleSheet('QPushButton {background-color: white; color: #222222}') # Изменение стилей
        con.close()
    # Функции, открыващие приложения из главного окна
    def calc(self) -> None:
        self.ex = Calculator()
        self.ex.show()

    def notepad(self) -> None:
        self.ex2 = Notepad()
        self.ex2.show()

    def random(self) -> None:
        self.ex3 = Randomnum()
        self.ex3.show()

    def calendar(self) -> None:
        self.ex4 = Calendar()
        self.ex4.show()

    def photoshop(self) -> None:
        self.ex5 = Photoshop()
        self.ex5.show()

    def paint(self) -> None:
        self.ex6 = Paint()
        self.ex6.show()

# Обработка исключений
def except_hook(cls, exception, traceback) -> None:
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__': # Если файл запускается как основная программа
    sys.excepthook = except_hook
    app = QApplication(sys.argv) # Создание приложения
    ex = WindowsProgram() # Создание окна
    ex.show() # Показ окна на экране
    sys.exit(app.exec()) # Выход
