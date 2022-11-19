# Импорт библиотек и классов
from PyQt5.QtWidgets import QWidget, QTextEdit, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QIcon
import sqlite3


class Notepad(QWidget):
    def __init__(self) -> None: # Инициализация
        super().__init__() # Инициализатор базового класса
        self.init_ui() # Вызов метода init_ui для настройки интерфейса и некоторых значений

    def init_ui(self) -> None:
        # Настройка окна, кнопок и лайаутов
        self.setStyleSheet("background-color: white;")
        # Получение начальных значений из бд
        con = sqlite3.connect('dbs/notes.db')
        self.names = [elem[0] for elem in con.execute('''SELECT title from notes''')]
        con.close() # Закрытие дб
        self.previous = ';nothing;'
        self.setGeometry(500, 500, 800, 400)
        self.setWindowTitle('Блокнот')
        self.setWindowIcon(QIcon('icons/notepad.jpg'))
        layout = QHBoxLayout()
        layout2 = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setFont(QFont('Arial', 10))
        self.btn_saveas = QPushButton('Сохранить как', self)
        self.btn_save = QPushButton('  Сохранить  ', self)
        self.btn_load = QPushButton('  Загрузить  ', self)
        self.btn_delete = QPushButton('   Удалить   ', self)
        self.btn_saveas.setStyleSheet('background-color: #121212; color: white')
        self.btn_save.setStyleSheet('background-color: #121212; color: white')
        self.btn_load.setStyleSheet('background-color: #121212; color: white')
        self.btn_delete.setStyleSheet('background-color: #121212; color: white')
        # # Подключение к методам кнопок
        self.btn_saveas.clicked.connect(self.save_as)
        self.btn_load.clicked.connect(self.load)
        self.btn_save.clicked.connect(self.save)
        self.btn_delete.clicked.connect(self.delete)
        # Настройка положений кнопок
        self.btn_delete.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.btn_saveas.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.btn_load.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.btn_save.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        # Добавление виджетов в лайауты и set лайаутов на основной виджет
        layout.addWidget(self.text)
        layout2.addWidget(self.btn_saveas)
        layout2.addWidget(self.btn_save)
        layout2.addWidget(self.btn_load)
        layout2.addWidget(self.btn_delete)
        layout.addLayout(layout2)
        self.setLayout(layout)
        self.setLayout(layout2)
    # Кнопка сохранения
    def save_as(self) -> None:
        name, ok_pressed = QInputDialog.getText(self, 'Имя файла', 'Введите имя файла:') # Получение имени файла
        if ok_pressed and name not in self.names:
            # Подключение к бд
            con = sqlite3.connect('dbs/notes.db')
            set_text = self.text.toPlainText() # Получение текста
            # Сохранение текста в бд под полученным именем файла
            result = con.execute('''INSERT INTO notes(title, text) VALUES (?, ?)''', (name, set_text,))
            self.names.append(name)
            con.commit() # Отправка новых данных в бд
            con.close()
            self.text.setText('')
        elif name in self.names: # Если введено существующее имя
            # Вывод ошибки
            msg = QMessageBox(self)
            msg.show()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка")
            msg.setInformativeText('Выбранное имя файла уже существует')
            msg.exec_()
    # Кнопка загрузки
    def load(self) -> None:
        # Подключение к бд
        con = sqlite3.connect('dbs/notes.db')
        result = con.execute('''SELECT title FROM notes''',) # Получение имен файлов
        name2, ok_pressed2 = QInputDialog.getItem(self, 'Имя файла', 'Выберите имя файла:',
                                                tuple([elem[0] for elem in result]), 0, False) # Выбор существ. имени
        # Если нажата кнопка "Ок"
        if ok_pressed2:
            res = [elem[0] for elem in con.execute('''SELECT text FROM notes WHERE title == ?''',
                                                             (name2,))][0]
            self.text.setText(
                f"{res}")
            self.previous = name2
        con.close()
    # Сохранение существующего
    def save(self) -> None:
        if self.previous == ';nothing;': # Если еще не было работы с сохранением
            self.save_as()
        else:
            # Подключение к бд
            con = sqlite3.connect('dbs/notes.db')
            set_text = self.text.toPlainText()
            # Обновление текста в бд под прошлым именем
            result = con.execute('''UPDATE notes SET text = ? WHERE title = ?''', (set_text, self.previous,))
            con.commit() # Отправка новых данных в бд
            con.close()
    # Кнопка удаления
    def delete(self) -> None:
        # Подключение к бд
        con = sqlite3.connect('dbs/notes.db')
        result = con.execute('''SELECT title FROM notes''', )
        name2, ok_pressed2 = QInputDialog.getItem(self, 'Имя файла', 'Выберите имя файла:',
                                                  tuple([elem[0] for elem in result]), 0, False) # Выбор существ. имени
        if ok_pressed2:
            con.execute('''DELETE FROM notes WHERE title == ?''', # Удаление данных из бд под выбранным именем
                                                   (name2,))
            con.commit() # Отправка новых данных в бд
            self.names.remove(name2)
        con.close()