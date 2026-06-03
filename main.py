import logging
import sys
from PyQt6.QtWidgets import QApplication
from app.models.test_model import TestModel
from app.viewers.main_window import MainWindow
from app.controllers.main_controller import MainController

def setup_logging():
    logging.basicConfig(
        filename = 'Optical_switch_test.log',
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        )

def main():
    setup_logging()
    app = QApplication(sys.argv)

    model = TestModel()
    view = MainWindow()
    controller = MainController(model, view)

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()