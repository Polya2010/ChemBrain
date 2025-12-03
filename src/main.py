import sys
from PyQt6.QtWidgets import QApplication
from chemistry_learning_app import ChemistryEducationApp


def start_application():
    application_instance = QApplication(sys.argv)
    application_instance.setStyle('Fusion')
    main_window_instance = ChemistryEducationApp()
    main_window_instance.show()
    sys.exit(application_instance.exec())


if __name__ == '__main__':
    start_application()
