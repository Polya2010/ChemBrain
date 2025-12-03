from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
)


class LoginDialog(QDialog):
    def __init__(self, account_manager):
        super().__init__()
        self.account_manager = account_manager
        self.setWindowTitle("ChemBrain - Авторизация")
        self.setModal(True)
        self._create_interface()

    def _create_interface(self):
        dialog_layout = QVBoxLayout()

        form_section = QFormLayout()

        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText(
            "Введите имя пользователя"
        )
        form_section.addRow("Имя пользователя:", self.username_field)

        dialog_layout.addLayout(form_section)

        button_section = QHBoxLayout()

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self._perform_login)
        button_section.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self._perform_registration)
        button_section.addWidget(self.register_button)

        self.exit_button = QPushButton("Выйти")
        self.exit_button.setStyleSheet(
            "background-color: #ff6666; color: white;"
        )
        self.exit_button.clicked.connect(self.reject)
        button_section.addWidget(self.exit_button)

        dialog_layout.addLayout(button_section)

        self.status_message = QLabel("")
        self.status_message.setStyleSheet("color: red;")
        dialog_layout.addWidget(self.status_message)

        self.setLayout(dialog_layout)

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
