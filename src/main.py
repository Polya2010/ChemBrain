import sys
from PyQt6.QtWidgets import QApplication
from chemistry_learning_app import ChemistryLearningApp

def launch_application():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = ChemistryLearningApp()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    launch_application()