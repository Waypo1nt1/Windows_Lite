# Импорт библиотек и классов
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PIL import Image
from PyQt5 import uic


class Photoshop(QWidget):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        uic.loadUi('ui/ps.ui', self) # Загрузка файла с дизайнера
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        # Настройка окна
        self.setWindowTitle('Фоторедактор')
        self.setWindowIcon(QIcon('icons/photoshop.png'))
        self.setFixedSize(700, 700)
        # Путь к файлу изначально равен пустой строке
        self.fname = ''
        while self.fname == '': # Пока не будет получено изображение
            self.fname = QFileDialog.getOpenFileName(self,
                                                     'Выберите изображение для работы (рек. 389 x 389)', '',
                                                     'Картинка (*.jpg);;Картинка (*.png)')[0]
            # Если не был выбран файл, то путь так и останется пустым
            if self.fname == '':
                # Вывод ошибки
                msg = QMessageBox(self)
                msg.setStyleSheet('background-color: white; color: black')
                msg.show()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Ошибка")
                msg.setText("Ошибка")
                msg.setInformativeText('Не выбрано ни одного изображения')
                msg.exec_()
        # Создание других переменных, показ выбранной картинки на экране
        self.fname2 = self.fname
        self.fname3 = self.fname
        self.pixmap = QPixmap(self.fname).scaled(389, 389)
        self.image = QLabel(self)
        self.verticalLayout.addWidget(self.image)
        self.image.setPixmap(self.pixmap)
        self.btn_left.setFont(QFont('Arial', 10))
        self.btn_right.setFont(QFont('Arial', 10))
        self.btn_default.setFont(QFont('Arial', 10))
        # Подключение кнопок к методам
        self.btn_R.clicked.connect(self.rgb)
        self.btn_G.clicked.connect(self.rgb)
        self.btn_B.clicked.connect(self.rgb)
        self.btn_default.clicked.connect(self.default)
        self.btn_right.clicked.connect(self.turn)
        self.btn_left.clicked.connect(self.turn)
        self.btn_remover.clicked.connect(self.removergb)
        self.btn_removeg.clicked.connect(self.removergb)
        self.btn_removeb.clicked.connect(self.removergb)
        self.btn_saveas.clicked.connect(self.save_as)
    # Изменение цветового канала (удаление двух)
    def rgb(self) -> None:
        im = Image.open(self.fname) # Открытие изображения
        pixels = im.load() # Загрузка пикселей
        x, y = im.size # Получение размеров изображения
        # Прохождение по пикселям, изменение цветовых каналов
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                rr, gr, br = r, 0, 0
                rb, gb, bb = 0, 0, b
                rg, gg, bg = 0, g, 0
                if self.sender() == self.btn_R:
                    pixels[i, j] = rr, gr, br
                    self.label.setText('Последний эффект: красный канал')
                elif self.sender() == self.btn_B:
                    pixels[i, j] = rb, gb, bb
                    self.label.setText('Последний эффект: синий канал')
                elif self.sender() == self.btn_G:
                    pixels[i, j] = rg, gg, bg
                    self.label.setText('Последний эффект: зелёный канал')
        im.save('pic.png', "PNG")
        self.fname2 = 'pic.png'
        self.pixmap = QPixmap(self.fname2)
        self.pixmap2 = self.pixmap.scaled(389, 389)
        self.image.setPixmap(self.pixmap2)
    # Изменение изображения по умолчанию
    def default(self) -> None:
        self.pixmap = QPixmap(self.fname3)
        self.pixmap2 = self.pixmap.scaled(389, 389)
        self.image.setPixmap(self.pixmap2)
        self.fname = self.fname3
        self.label.setText('')
    # Поворот изображения
    def turn(self) -> None:
        if self.sender() == self.btn_left:
            # Открытие картинок и поворот влево
            im = Image.open(self.fname2)
            im_d = Image.open(self.fname) # Вспомогательное изображение с стандартным цветовым каналом
            im_d = im_d.transpose(Image.Transpose.ROTATE_90)
            im = im.transpose(Image.Transpose.ROTATE_90)
            self.label.setText('Последний эффект: изображение повёрнуто влево')
        elif self.sender() == self.btn_right:
            # Открытие картинок и поворот вправо
            im = Image.open(self.fname2)
            im_d = Image.open(self.fname) # Вспомогательное изображение с стандартным цветовым каналом
            im_d = im_d.transpose(Image.Transpose.ROTATE_270)
            im = im.transpose(Image.Transpose.ROTATE_270)
            self.label.setText('Последний эффект: изображение повёрнуто вправо')
        im.save('pic.png', "PNG")
        im_d.save('pic_default_color', "PNG")
        self.fname2 = 'pic.png'
        self.fname = 'pic_default_color'
        self.pixmap = QPixmap(self.fname2).scaled(389, 389)
        self.image.setPixmap(self.pixmap)
    # Изменение цветового канала (удаление одного из)
    def removergb(self) -> None:
        im = Image.open(self.fname) # Открытие изображения
        pixels = im.load() # Загрузка пикселей
        x, y = im.size # Получение размеров изображения
        # Прохождение по пикселям, изменение цветовых каналов
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                rr, gr, br = 0, g, b
                rb, gb, bb = r, g, 0
                rg, gg, bg = r, 0, b
                if self.sender() == self.btn_remover:
                    pixels[i, j] = rr, gr, br
                    self.label.setText('Последний эффект: убран красный канал')
                elif self.sender() == self.btn_removeb:
                    pixels[i, j] = rb, gb, bb
                    self.label.setText('Последний эффект: убран синий канал')
                elif self.sender() == self.btn_removeg:
                    pixels[i, j] = rg, gg, bg
                    self.label.setText('Последний эффект: убран зелёный канал')
        # Промежуточное сохранение картинки и показ новой на окне
        im.save('pic.png', "PNG")
        self.fname2 = 'pic.png'
        self.pixmap = QPixmap(self.fname2)
        self.pixmap2 = self.pixmap.scaled(389, 389)
        self.image.setPixmap(self.pixmap2)
    # Сохранение изображения
    def save_as(self) -> None:
        if self.fname2:
            filePath, ok_pressed = QFileDialog.getSaveFileName(self, "Сохранить картинку", "",
                                                      "Картинка (*.jpg);;Картинка (*.png)")
            if ok_pressed:
                self.pixmap.save(filePath)