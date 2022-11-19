# Импорт библиотек и классов
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

# Калькулятор
class Calculator(QWidget):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        # Создание виджетов, переменных, настройка виджетов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.eq)
        self.signs = '+-*/'
        self.setFixedSize(280, 450)
        self.setWindowTitle('Калькулятор')
        self.setWindowIcon(QIcon('icons/Calcul.png'))
        self.setStyleSheet('background-color: white')

        self.btn1 = QPushButton('1', self)
        self.btn2 = QPushButton('2', self)
        self.btn3 = QPushButton('3', self)
        self.btn4 = QPushButton('4', self)
        self.btn5 = QPushButton('5', self)
        self.btn6 = QPushButton('6', self)
        self.btn7 = QPushButton('7', self)
        self.btn8 = QPushButton('8', self)
        self.btn9 = QPushButton('9', self)
        self.btnC = QPushButton('C', self)
        self.btn0 = QPushButton('0', self)
        self.btnsnum = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9,
                     self.btn0]
        self.btnCE = QPushButton('CE', self)
        self.btndiv = QPushButton('/', self)
        self.btnmult = QPushButton('*', self)
        self.btnmn = QPushButton('-', self)
        self.btnpl = QPushButton('+', self)
        self.btndot = QPushButton('.', self)
        self.btnplmn = QPushButton('±', self)
        self.btnravn = QPushButton('=', self)
        self.btnssign = [self.btndiv, self.btnmult, self.btnmn, self.btnpl]
        self.label = QLabel('0', self)
        self.label2 = QLabel('', self)
        self.labeltext = '0'
        self.label2text = '0'
        self.flag = False
        self.flag2 = False
        self.flag3 = False
        # Привязка событий нажатия кнопок к соответствующим методам
        for elem in self.btnsnum:
            elem.clicked.connect(self.numb)
        self.btnC.clicked.connect(self.clear)
        self.btnCE.clicked.connect(self.clear)
        for elem in self.btnssign:
            elem.clicked.connect(self.op)
        self.btnravn.clicked.connect(self.eq)
        self.btnplmn.clicked.connect(self.mnpl)
        self.btndot.clicked.connect(self.numb)
        # Изменение размеров и положения
        self.btn1.setGeometry(0, 240, 70, 70)
        self.btn2.setGeometry(70, 240, 70, 70)
        self.btn3.setGeometry(140, 240, 70, 70)
        self.btn4.setGeometry(0, 170, 70, 70)
        self.btn5.setGeometry(70, 170, 70, 70)
        self.btn6.setGeometry(140, 170, 70, 70)
        self.btn7.setGeometry(0, 100, 70, 70)
        self.btn8.setGeometry(70, 100, 70, 70)
        self.btn9.setGeometry(140, 100, 70, 70)
        self.btnC.setGeometry(0, 310, 70, 70)
        self.btn0.setGeometry(70, 310, 70, 70)
        self.btnCE.setGeometry(140, 310, 70, 70)
        self.btndiv.setGeometry(210, 100, 70, 70)
        self.btnmult.setGeometry(210, 170, 70, 70)
        self.btnmn.setGeometry(210, 240, 70, 70)
        self.btnpl.setGeometry(210, 310, 70, 70)
        self.btndot.setGeometry(0, 380, 70, 70)
        self.btnplmn.setGeometry(70, 380, 70, 70)
        self.btnravn.setGeometry(140, 380, 140, 70)
        self.label.setGeometry(0, 20, 280, 80)
        self.label2.setGeometry(0, 0, 280, 20)
        self.label.setFont(QFont('Arial', 50))
        self.label2.setFont(QFont('Arial', 10))
        self.label.setAlignment(Qt.AlignRight)
        self.label2.setAlignment(Qt.AlignRight)
    # Обрабатывает нажатия для кнопок с цифрами и кнопки с точкой
    def numb(self) -> None:
        # Проверка наличия точки в выражении при нажатой точке
        if self.sender() == self.btndot and '.' in self.labeltext:
            return # Если точка уже есть, ничего не делаем и не возвращаем
        if not self.flag: # Если не была нажата кнопка операции
            if self.flag3: # Если уже был начат ввод значений
                if self.labeltext != '0':
                    self.labeltext += self.sender().text()
                else:
                    self.labeltext = '' if self.sender() != self.btndot else f'0{self.sender().text()}'
                    self.labeltext += self.sender().text()
            elif self.sender() != self.btn0: # Если
                self.flag3 = True # Был начат ввод значений
                self.labeltext = ''
                self.labeltext += self.sender().text() if self.sender() != self.btndot else f'0{self.sender().text()}'
            self.label.setText(self.labeltext)
        elif self.flag and not self.flag2:
            self.labeltext = ''
            self.labeltext += self.sender().text() if self.sender() != self.btndot else f'0{self.sender().text()}'
            self.label.setText(self.labeltext)
            self.flag2 = True # Нажаты кнопки цифр или точек после нажатой кнопки операции
        else:
            self.labeltext += self.sender().text()
            self.label.setText(self.labeltext)

    # При нажатии на кнопки C и CE
    def clear(self) -> None:
        # Обнуление переменных до их первоначальных значений
        self.labeltext = '0'
        self.label2.setText('')
        self.label2text = '0'
        self.label.setText(self.labeltext)
        self.flag = False
        self.flag2 = False
        self.flag3 = False

    def op(self) -> None: # При нажатии на кнопки операций
        # Изменение знака операции
        if self.flag and self.sender().text() != self.label2.text()[-1] and not self.flag2:
            if '.' in self.label2text:
                self.label2text = self.label2text[:-5]
            else:
                self.label2text = self.label2text[:-3]
        if self.label.text() != '0' and self.label2text[-1] != self.sender().text():
            # Если были нажаты кнопки цифр или точек после нажатия кнопки операции и снова нажата кнопка операции
            if self.flag2:
                self.eq()
            # В другом случае
            else:
                self.label2.setText(f'{self.label.text()}{self.sender().text()}')
                self.label2text += f'{self.label.text()}{self.sender().text()}'
                self.flag = True # При нажатии на кнопку операции в первый раз

    def eq(self) -> None: # Получение результата и его вывод
        if self.sender() == self.timer:
            self.timer.stop() # Остановка таймера
        if self.flag2:
            try:
                self.labeltext = eval(self.label2text[1:] + self.labeltext)
                self.labeltext = "{:.2f}".format(self.labeltext).rstrip('0') if \
                    type(self.labeltext) == float and int(self.labeltext) != self.labeltext else str(int(self.labeltext))
                self.label.setText(f'{self.labeltext}')
                self.label2.setText('')
                self.label2text = '0'
            except ZeroDivisionError:
                # При попытке деления на ноль старт таймера для показа ошибки на некоторое время
                self.label.setText('error')
                self.timer.start(300)
        else:
            self.label.setText(f"{self.labeltext.rstrip('0').rstrip('.')}" if '.' in self.labeltext else
                               f"{self.labeltext.rstrip('.')}")
            self.label2.setText('')
            self.label2text = '0'
        self.flag = False
        self.flag2 = False
        self.flag3 = False

    def mnpl(self) -> None:
        # Метод изменения знака числа
        if self.label.text() != '0':
            self.label2.setText('')
            self.label2text = '0'
            if len(self.labeltext) <= 2 and '.' in self.labeltext:
                return
            else:
                self.labeltext = '-' + self.labeltext if float(self.labeltext) > 0 else self.labeltext[1:]
                self.label.setText(f'-{self.label.text()}' if float(self.label.text()) > 0 else f'{self.label.text()[1:]}')
                self.flag = False
                self.flag2 = False
                self.flag3 = False
