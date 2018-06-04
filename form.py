import os
from PyQt5 import QtCore, QtWidgets, QtGui


class MainWindow(QtWidgets.QWidget):
    """
    Главное окно.
    """

    def __init__(self, device, weather, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.device = device
        self.weather = weather
        self.port = None

        self.setFixedSize(400, 300)

        ico = QtGui.QIcon(os.path.join("icons", "arduino_weather_notification.png"))
        self.setWindowIcon(ico)

        # Страницы для QStackedWidget.
        self.stack_connect = QtWidgets.QWidget()
        self.stack_menu = QtWidgets.QWidget()
        self.stack_weather = QtWidgets.QWidget()
        self.stack_manual = QtWidgets.QWidget()

        # Стек страниц из виджетов
        self.stack_widget = QtWidgets.QStackedWidget(self)
        self.stack_widget.addWidget(self.stack_connect)
        self.stack_widget.addWidget(self.stack_menu)
        self.stack_widget.addWidget(self.stack_weather)
        self.stack_widget.addWidget(self.stack_manual)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(self.stack_widget)
        self.setLayout(self.grid_layout)

        self.go_change_page(0)

    def connect_page(self):
        """
        Страница подключения к СОМ порту.
        :return:
        """
        lbl_select = QtWidgets.QLabel("<b>Which port device connection?</b>",
                                    alignment=QtCore.Qt.AlignCenter)

        btn_refresh = QtWidgets.QPushButton(
            QtGui.QIcon(os.path.join("icons", "refresh.png")), None)
        btn_refresh.setToolTip("Refresh")

        list_box = QtWidgets.QListWidget()
        btn_connect = QtWidgets.QPushButton("&Connect")
        self.serial_ports_views(list_box)

        horizontal_spacer = QtWidgets.QSpacerItem(140, 20,
                                                  QtWidgets.QSizePolicy.Minimum,
                                                  QtWidgets.QSizePolicy.Expanding)

        horizontal_layout_top = QtWidgets.QHBoxLayout()
        horizontal_layout_top.addWidget(lbl_select)
        horizontal_layout_top.addSpacerItem(horizontal_spacer)
        horizontal_layout_top.addWidget(btn_refresh)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout_top)
        vertical_layout.addWidget(list_box)
        vertical_layout.addWidget(btn_connect)

        self.stack_connect.setLayout(vertical_layout)

        list_box.itemClicked.connect(self.on_item_clicked)
        btn_connect.clicked.connect(self.on_connect_button)
        btn_refresh.clicked.connect(
            lambda: self.serial_ports_views(list_box))

    def menu_page(self):
        """
        Страница главного меню приложения.
        :return:
        """
        btn_weather = QtWidgets.QPushButton("&Weather")
        btn_weather.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Expanding)
        btn_manual = QtWidgets.QPushButton("&Manual")
        btn_manual.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                 QtWidgets.QSizePolicy.Expanding)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(btn_weather)
        vertical_layout.addWidget(btn_manual)

        self.stack_menu.setLayout(vertical_layout)

        btn_weather.clicked.connect(lambda: self.go_change_page(2))
        btn_manual.clicked.connect(lambda: self.go_change_page(3))

    def weather_page(self):
        """
        Страница погодных данных с wundergroung.com с реакцией куба
        на вероятность дождя.
        :return:
        """
        weather_data = self.weather.check_weather()
        self.check_internet_connection()

        lbl_date = QtWidgets.QLabel("<b>" +
                                    weather_data[0] + "/" +
                                    weather_data[1] + "/" +
                                    weather_data[2] + "</b>",
                                    alignment=QtCore.Qt.AlignRight)
        lbl_weekday = QtWidgets.QLabel("<b>" + weather_data[3] + "</b>",
                                       alignment=QtCore.Qt.AlignCenter)
        lbl_temp = QtWidgets.QLabel(
            "<b>Temperature: " + weather_data[4] + "</b>")
        lbl_wind = QtWidgets.QLabel("<b>Wind: " + weather_data[5] + "</b>")
        lbl_pop = QtWidgets.QLabel(
            "<b>Probability of Precipitation: " + weather_data[6] + "</b>")

        btn_back = QtWidgets.QPushButton("&Back")
        horizontal_spacer = QtWidgets.QSpacerItem(40, 20,
                                                  QtWidgets.QSizePolicy.Expanding)

        horizontal_layout_0 = QtWidgets.QHBoxLayout()
        horizontal_layout_0.addItem(horizontal_spacer)
        horizontal_layout_0.addWidget(btn_back)

        vertical_layout_0 = QtWidgets.QVBoxLayout()
        vertical_layout_0.addWidget(lbl_date)
        vertical_layout_0.addWidget(lbl_weekday)
        vertical_layout_0.addWidget(lbl_temp)
        vertical_layout_0.addWidget(lbl_wind)
        vertical_layout_0.addWidget(lbl_pop)
        vertical_layout_0.addLayout(horizontal_layout_0)

        self.stack_weather.setLayout(vertical_layout_0)

        if isinstance(weather_data[7], int):
            if weather_data[7] <= 30:
                self.turn_led_green()
            else:
                self.turn_led_red()

        btn_back.clicked.connect(lambda: self.go_change_page(1))

    def manual_page(self):
        """
        Страница для ручного управления кубом.
        :return:
        """
        btn_green = QtWidgets.QPushButton("&Green")
        btn_green.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                QtWidgets.QSizePolicy.Expanding)
        btn_red = QtWidgets.QPushButton("&Red")
        btn_red.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                              QtWidgets.QSizePolicy.Expanding)
        btn_blink = QtWidgets.QPushButton("&Blink")
        btn_blink.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                QtWidgets.QSizePolicy.Expanding)
        btn_back = QtWidgets.QPushButton("&Back")
        horizontal_spacer = QtWidgets.QSpacerItem(40, 20,
                                                  QtWidgets.QSizePolicy.Expanding)

        vertical_layout_0 = QtWidgets.QVBoxLayout()
        vertical_layout_0.addWidget(btn_green)
        vertical_layout_0.addWidget(btn_red)
        vertical_layout_0.addWidget(btn_blink)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addItem(horizontal_spacer)
        horizontal_layout.addWidget(btn_back)

        vertical_layout_1 = QtWidgets.QVBoxLayout()
        vertical_layout_1.addLayout(vertical_layout_0)
        vertical_layout_1.addLayout(horizontal_layout)

        self.stack_manual.setLayout(vertical_layout_1)

        btn_green.clicked.connect(self.on_green_button)
        btn_red.clicked.connect(self.on_red_button)
        btn_blink.clicked.connect(self.on_blink_button)
        btn_back.clicked.connect(lambda: self.go_change_page(1))

    def closeEvent(self, e):
        """
        Обработка закрытия окна.
        :param e:
        :return:
        """
        result = QtWidgets.QMessageBox.question(self,
                                                self.windowTitle(),
                                                "Are you sure you want to exit?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            if self.device.is_connected():
                self.device.disconnect()
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()

    @QtCore.pyqtSlot()
    def serial_ports_views(self, list_box):
        """
        Заполнение List Widget списком доступных портов.
        :param list_box: объект QListWidget
        :return:
        """
        ports = self.device.discover()
        list_box.clear()

        for port in ports:
            list_box.addItem(port)

        if list_box.count() > 0:
            list_box.setCurrentItem(list_box.item(0))
            self.port = list_box.item(0).text()

    def check_internet_connection(self):
        """
        Проверяет есть ли соединение с интернетом.
        :return:
        """
        if self.weather.connection_error_flag:
            QtWidgets.QMessageBox.warning(self, self.windowTitle(),
                                          "No internet connection.\n"
                                          "Weather data will be not showing.",
                                          QtWidgets.QMessageBox.Ok)

    @QtCore.pyqtSlot(int)
    def go_change_page(self, index):
        """
        Переход по страницам главного окна.
        :param index: Индекс страницы.
        :return:
        """
        if index == 0:
            self.connect_page()
        elif index == 1:
            self.menu_page()
            self.device.disconnect()
        elif index == 2:
            self.weather_page()
        elif index == 3:
            self.manual_page()

        self.stack_widget.setCurrentIndex(index)

    @QtCore.pyqtSlot()
    def on_item_clicked(self):
        """
        Присваивает имя выбранного в ListWidget COM порта
        переменной self.port.
        :return:
        """
        self.port = self.sender().currentItem().text()

    @QtCore.pyqtSlot()
    def on_connect_button(self):
        """
        Открывает поток на подключение к устройству.
        :return:
        """
        if self.port is None:
            QtWidgets.QMessageBox.warning(self, self.windowTitle(),
                                          "Select Arduino port!",
                                          QtWidgets.QMessageBox.Ok)
        else:
            self.device.connect(self.port)
            self.go_change_page(1)

    @QtCore.pyqtSlot(name="turn_led_red")
    def on_red_button(self):
        """
        Зажигает красные диоды.
        :return:
        """
        self.device.go_red()

    @QtCore.pyqtSlot(name="turn_led_green")
    def on_green_button(self):
        """
        Зажигает зеленые диоды.
        :return:
        """
        self.device.go_green()

    @QtCore.pyqtSlot()
    def on_blink_button(self):
        """
        Мигает светодиодами по очереди.
        :return:
        """
        self.device.blink()


if __name__ == "__main__":
    print("Это модуль формы")
