from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginDialog(QDialog):
    def __init__(self, account_manager, parent=None):
        super().__init__(parent)
        self.account_manager = account_manager
        self.setWindowTitle("ChemBrain - Авторизация")
        self.setModal(True)
        self.setFixedSize(400, 200)
        self._create_interface()

    def _create_interface(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title_label = QLabel("ChemBrain - Обучение химии")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Введите имя пользователя")
        self.username_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow("👤 Имя пользователя:", self.username_field)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        login_button = QPushButton("Войти")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        login_button.clicked.connect(self._perform_login)
        buttons_layout.addWidget(login_button)
        
        register_button = QPushButton("Регистрация")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        register_button.clicked.connect(self._perform_registration)
        buttons_layout.addWidget(register_button)
        
        exit_button = QPushButton("Выйти")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_button.clicked.connect(self.reject)
        buttons_layout.addWidget(exit_button)
        
        layout.addLayout(buttons_layout)
        
        self.status_message = QLabel("")
        self.status_message.setStyleSheet("color: #e74c3c; font-size: 12px; margin-top: 5px;")
        self.status_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_message)

    def _perform_login(self):
        input_username = self.username_field.text().strip()
        if not input_username:
            self.status_message.setText("Введите имя пользователя")
            return

        login_success, message_text = (
            self.account_manager.verify_user(input_username)
        )
        if login_success:
            self.accept()
        else:
            self.status_message.setText(message_text)

    def _perform_registration(self):
        input_username = self.username_field.text().strip()
        if not input_username:
            self.status_message.setText("Введите имя пользователя")
            return

        registration_success, message_text = (
            self.account_manager.create_new_account(input_username)
        )
        if registration_success:
            self.accept()
        else:
            self.status_message.setText(message_text)