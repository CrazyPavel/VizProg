import traceback
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QTableWidgetItem , QLabel, QFileDialog
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QSettings, Qt, QByteArray
from kalendar import Ui_MainWindow
from db import DatabaseManager
import sys
import pickle

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("YourCompany", "YourApp")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image_data = None
        # Инициализация базы данных
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()

        # self.db_manager.create_tables_1()
        # Инициализация модели для таблицы birthdays
        self.model_birthdays = QSqlTableModel()
        self.model_birthdays.setTable('birthdays')
        self.model_birthdays.select()
        #Обработчик для нажатий на шапку столбца
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.setColumnWidth(1, 200)
        self.ui.tableWidget.setColumnWidth(2, 200)
        self.ui.tableWidget.setColumnWidth(3, 200)
        self.ui.tableWidget.setColumnWidth(4, 205)
        #Удаление ячеек
        self.ui.pushButton_3.clicked.connect(self.delete_selected_birthday)
        self.ui.pushButton_3.clicked.connect(self.updateTableFromDatabase)
        # Поиск по таблице
        self.ui.lineEdit_2.setPlaceholderText('Введите текст для поиска')
        self.ui.lineEdit_2.textChanged.connect(self.filterTable)
        # Подключение событий к методам
        self.ui.pushButton_2.clicked.connect(self.on_click)
        self.ui.pushButton_2.clicked.connect(self.populateTableFromDatabase1)
        # Выпадающая панель
        self.load_items_from_settings()
        self.ui.pushButton_7.clicked.connect(self.add_item)
        self.ui.pushButton_8.clicked.connect(self.clear_items)
        #Загрузка картинки
        self.ui.pushButton_6.clicked.connect(self.browseImage)
        self.ui.calendarWidget.clicked.connect(self.on_click_calendar)
        self.ui.dateEdit.dateChanged.connect(self.on_dateedit_change)
        # Заполнение начальных значений
        self.ui.tableWidget.setColumnWidth(0, 104)
        self.start_date = self.ui.calendarWidget.selectedDate()
        self.now_date = self.ui.calendarWidget.selectedDate()
        self.time_date = self.ui.calendarWidget.selectedDate()
        self.description = self.ui.plainTextEdit.toPlainText()
        # self.read_from_file()
        self.populateTableFromDatabase1()
        self.ui.label_4.setText("Дата: %s " % self.now_date.toString('dd-MM-yyyy'))
        self.on_click_calendar()

    def populateTableFromDatabase1_1(self):
        print("Populating table...")
        data = self.db_manager.fetch_data_from_database()
        self.ui.tableWidget.setRowCount(0)

        if data:
            self.ui.tableWidget.setRowCount(len(data))
            self.ui.tableWidget.setColumnCount(len(data[0]))

            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    if col_num == 4:
                        pixmap = QPixmap()
                        try:
                            byte_array = QByteArray(col_data)
                            pixmap.loadFromData(byte_array)
                            # расширение картинки в поле tablewidget
                            scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)

                            image_label = QLabel()
                            image_label.setPixmap(scaled_pixmap)
                            image_label.setAlignment(Qt.AlignCenter)

                            self.ui.tableWidget.setCellWidget(row_num, col_num, image_label)
                            self.ui.tableWidget.setRowHeight(row_num, 150)
                            self.ui.tableWidget.setColumnWidth(col_num, 150)
                        except Exception as e:
                            print(f"Error processing image data: {e}")
                    else:
                        # Обычный текстовый элемент, если не изображение
                        item = QTableWidgetItem(str(col_data))
                        self.ui.tableWidget.setItem(row_num, col_num, item)

        self.db_manager.conn.commit()

    def updateTableFromDatabase(self):
        print("Updating table...")
        self.populateTableFromDatabase1_1()

    def populateTableFromDatabase1(self):
        data = self.db_manager.fetch_data_from_database()
        if data:
            self.ui.tableWidget.setRowCount(len(data))
            self.ui.tableWidget.setColumnCount(len(data[0]))

            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    if col_num == 4:
                        pixmap = QPixmap()
                        try:
                            byte_array = QByteArray(col_data)
                            pixmap.loadFromData(byte_array)
                            #расширение картинки в поле tablewidget
                            scaled_pixmap = pixmap.scaled(173, 173, Qt.KeepAspectRatio)

                            image_label = QLabel()
                            image_label.setPixmap(scaled_pixmap)
                            image_label.setAlignment(Qt.AlignCenter)

                            self.ui.tableWidget.setCellWidget(row_num, col_num, image_label)
                            self.ui.tableWidget.setRowHeight(row_num, 173)
                            self.ui.tableWidget.setColumnWidth(col_num, 173)
                        except Exception as e:
                            print(f"Error processing image data: {e}")

                    else:
                        if col_num == 4:
                            font = QFont()
                            font.setPointSize(14)
                            item.setFont(font)

                        item = QTableWidgetItem(str(col_data))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget.setItem(row_num, col_num, item)

            self.db_manager.conn.commit()

    # def save_to_file(self):
    #     data_to_save = {"start": self.start_date, "end": self.time_date, "desc": self.description,
    #                     "Secname": self.description_1}
    #     file1 = open(os.path.join("date.txt"), "wb")
    #     pickle.dump(data_to_save, file1)
    #     file1.close()

    # def read_from_file(self):
    #     try:
    #         file1 = open(os.path.join("date.txt"), "rb")
    #         data_to_load = pickle.load(file1)
    #         file1.close()
    #         self.start_date = data_to_load["start"]
    #         self.time_date = data_to_load["end"]
    #         self.description = data_to_load["desc"]
    #         self.description_1 = data_to_load["Secname"]
    #         print(self.start_date.toString('dd-MM-yyyy'), self.time_date.toString('dd-MM-yyyy'),
    #                 self.description, self.description_1)
    #         self.ui.calendarWidget.setSelectedDate(self.time_date)
    #         self.ui.dateEdit.setDate(self.time_date)
    #         self.ui.plainTextEdit.setPlainText(self.description)
    #         delta_days_left = self.start_date.daysTo(self.now_date)  # прошло дней
    #         delta_days_right = self.now_date.daysTo(self.time_date)  # осталось дней
    #         days_total = self.start_date.daysTo(self.time_date)  # всего дней
    #
    #         procent = int(delta_days_left * 100 / days_total)
    #         self.ui.progressBar.setProperty("value", procent)
    #     except FileNotFoundError:
    #         print("Нет файла")

    #Диалоговое окно для выбора изображения
    def browseImage(self):
        # Диалоговое окно для выбора изображения
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Images (*.png *.jpg *.bmp)')

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "rb") as image_file:
                    self.image_data = image_file.read()

                pixmap = QPixmap(file_path)
                pixmap = pixmap.scaledToWidth(130)
                self.ui.label_6.setPixmap(pixmap)
                self.ui.label_6.setAlignment(Qt.AlignCenter)
            except Exception as e:
                print(f"Ошибка при загрузке изображения: {e}")

    def on_click(self):
        try:
            self.start_date = self.now_date
            self.time_date = self.ui.calendarWidget.selectedDate()
            self.description = self.ui.plainTextEdit.toPlainText()
            self.selected_text = self.ui.comboBox.currentText()
            self.left = self.start_date.daysTo(self.time_date)
            image_data = self.image_data if self.image_data is not None else None
            people = [(self.selected_text, self.description, self.time_date.toString('dd-MM-yyyy'), self.left,image_data)]
            self.db_manager.add_birthday(people)
            self.db_manager.conn.commit()
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            traceback.print_exc()


    def on_click_calendar(self):
        self.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
        self.time_date = self.ui.calendarWidget.selectedDate()
        delta_days = self.start_date.daysTo(self.time_date)
        self.ui.label_3.setText("До наступления события: %s дней" % delta_days)

    def on_dateedit_change(self):
        self.ui.calendarWidget.setSelectedDate(self.ui.dateEdit.date())
        self.time_date = self.ui.dateEdit.date()
        delta_days = self.start_date.daysTo(self.time_date)
        self.ui.label_3.setText("До наступления события: %s дней" % delta_days)

    #Выпадающая панель
    def add_item(self):
        new_item_text = self.ui.lineEdit.text()
        if new_item_text:
            self.ui.comboBox.insertItem(0, new_item_text)
            self.ui.comboBox.setCurrentIndex(0)
            self.ui.lineEdit.clear()
            self.save_items_to_settings()

    def clear_items(self):
        self.ui.comboBox.clear()
        self.save_items_to_settings()

    def load_items_from_settings(self):
        items = self.settings.value("items", [])
        self.ui.comboBox.addItems(items)

    def save_items_to_settings(self):
        items = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]
        self.settings.setValue("items", items)

    #поиск по таблице
    def filterTable(self):
        filter_text = self.ui.lineEdit_2.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            row_text = ' '.join([self.ui.tableWidget.item(row, col).text().lower() for col in
                                 range(4)])
            if filter_text in row_text:
                self.ui.tableWidget.setRowHidden(row, False)
            else:
                self.ui.tableWidget.setRowHidden(row, True)

    #Кнопка удаления
    def delete_selected_birthday(self):
        current_row = self.ui.tableWidget.currentRow()
        if current_row != -1:
            self.db_manager.delete_data_by_row(current_row)
            self.populateTableFromDatabase1()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
