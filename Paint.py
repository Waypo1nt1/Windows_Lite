# Импорт библиотек и классов
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QInputDialog, QFileDialog, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QSize, QPoint
from PIL import Image

class Paint(QMainWindow):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        # Настройка окна и меню
        self.new_func()
        self.setWindowTitle('Рисовальщик')
        self.setGeometry(300, 300, self.width, self.height)
        self.setMinimumSize(450, 300)
        self.setWindowIcon(QIcon('icons/paint.png'))
        self.setStyleSheet('background-color: #121212; color: white;')
        self.menu = self.menuBar()
        self.file = self.menu.addMenu('Файл')
        self.menu.setStyleSheet('QMenuBar::item {background-color: transparent}')
        self.brush_s = self.menu.addAction('Размер кисти')
        self.brush_c = self.menu.addAction('Цвет кисти')
        self.save = self.file.addAction('Сохранить')
        self.clear = self.file.addAction('Очистить')
        self.load = self.file.addAction('Загрузить')
        self.new = self.file.addAction('Новый холст')
        # Подключение к методам кнопок на меню
        self.brush_s.triggered.connect(self.set_size)
        self.brush_c.triggered.connect(self.set_color)
        self.clear.triggered.connect(self.clear_func)
        self.save.triggered.connect(self.save_func)
        self.load.triggered.connect(self.load_func)
        self.new.triggered.connect(self.new_func)
        # Переменные
        self.do_paint = False
        self.brush_size = 4
        self.brush_color = Qt.black
        self.x, self.y = 0, 0
        self.clcoordx, self.clcoordy = 0, 0

    def mouseMoveEvent(self, event) -> None: # Метод, срабатывающий при движении мышью
        self.x, self.y = event.x(), event.y() # Получение координат курсора
        if self.do_paint: # Если нужно рисовать
            qpi = QPainter(self.image) # Рисунок будет происходить по QImage
            qpi.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine)) # Настройка пера (ручки)
            qpi.drawLine(QPoint(self.clcoordx, self.clcoordy), QPoint(self.x, self.y)) # Создание рисунка по мыши
            self.clcoordx, self.clcoordy = event.x(), event.y() # Получение следующих координат
            self.repaint() # Вызов paintEvent, чтобы добавить на холст новые рисунки

    def paintEvent(self, event) -> None:
        # Обновление холста
        qp = QPainter(self)
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()

    def mousePressEvent(self, event) -> None: # При нажатии на мышку
        if event.button() == Qt.LeftButton: # Если это левая кнопка мыши
            self.x, self.y = event.x(), event.y() # Получение координат
            self.do_paint = True # При нажатой левой кнопки мыши можно рисовать
            self.clcoordx = self.x
            self.clcoordy = self.y

    def mouseReleaseEvent(self, event) -> None: # Когда клавиша на мышке отпущена
        if event.button() == Qt.LeftButton: # Если это левая кнопка мыши
            self.do_paint = False # Когда отпускается левая кнопка мыши нельзя рисовать

    def set_size(self) -> None:
        # Настройка размера кисти
        size, ok_pressed = QInputDialog.getInt(QWidget(), "Введите размер кисти", "Размер кисти:", 4, 2, 20, 1)
        if ok_pressed:
            self.brush_size = size

    def set_color(self) -> None:
        # Настройка цвета
        color = QColorDialog.getColor()
        self.brush_color = color

    def clear_func(self) -> None:
        # Очистка холста
        self.image.fill(Qt.white)
        self.repaint()

    def save_func(self) -> None:
        # Сохранение картинки в .jpg или в .png
        file, ok_pressed = QFileDialog.getSaveFileName(self, "Сохранить рисунок", "",
                                                      "Картинка (*.jpg);;Картинка (*.png)")
        if ok_pressed:
            self.image.save(file)

    def load_func(self) -> None:
        # Загрузка своего изображения
        file, ok_pressed = QFileDialog.getOpenFileName(self, "Выберите изображение (макс. 1920 x 1080)", "",
                                                           "Картинка (*.jpg);;Картинка (*.png)")
        if ok_pressed:
            self.loaded_image = file
            width, height = Image.open(self.loaded_image).size
            if width <= 1920 and height <= 1080:
                self.image = QImage(self.loaded_image)
            else:
                msg = QMessageBox(self)
                msg.setStyleSheet('background-color: white; color: black')
                msg.show()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Ошибка")
                msg.setText("Ошибка")
                msg.setInformativeText('Неподходящее разрешение изображения')
                msg.exec_()
                return
            self.repaint()

    def new_func(self) -> None:
        # Инициализация окна при запуске или нажатии на кнопку "новый холст", получение размеров холста
        ok_pressed = False
        ok_pressed2 = False
        self.loaded_image = QImage.Format_RGB32
        while not(ok_pressed and ok_pressed2): # Пока не будут введены размеры холста (нажаты все "Ок")
            num, ok_pressed = QInputDialog().getInt(self, "Введите ширину", "Ширина файла:", 1280, 900, 1920, 10)
            if ok_pressed:
                self.width = num
                num, ok_pressed2 = QInputDialog().getInt(self, "Введите высоту", "Высота файла:", 720, 600, 1080, 10)
                if ok_pressed2:
                    self.height = num
        self.image = QImage(QSize(self.width, self.height), self.loaded_image)
        self.image.fill(Qt.white)
        self.repaint()