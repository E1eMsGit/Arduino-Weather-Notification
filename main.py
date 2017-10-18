import sys
from PyQt5 import QtWidgets

from form import MainWindow
from device import WeatherCube
from weather_api import WeatherApi


def main():
    """
    Главная функция.
    Отвечает за запуск и работу приложения.
    :return:
    """
    app = QtWidgets.QApplication(sys.argv)
    device = WeatherCube()
    weather = WeatherApi()
    window = MainWindow(device, weather)

    window.setWindowTitle("Погодный куб")
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()