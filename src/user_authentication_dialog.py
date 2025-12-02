from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QHBoxLayout, QLabel
)

class UserAuthenticationDialog(QDialog):
    def __init__(self, user_manager):
        super().__init__()
        self.user_account_manager = user_manager
        self.setWindowTitle("ChemBrain - Вход в систему")
        self.setModal(True)
        self.initialize_dialog_interface()
    
    def initialize_dialog_interface(self):
        dialog_layout = QVBoxLayout()
        
        input_form_layout = QFormLayout()
        
        self.username_input_field = QLineEdit()
        self.username_input_field.setPlaceholderText("Введите имя пользователя")
        input_form_layout.addRow("Имя пользователя:", self.username_input_field)
        
        dialog_layout.addLayout(input_form_layout)
        
        action_buttons_layout = QHBoxLayout()
        
        self.login_action_button = QPushButton("Войти")
        self.login_action_button.clicked.connect(self.authenticate_user)
        action_buttons_layout.addWidget(self.login_action_button)
        
        self.registration_action_button = QPushButton("Зарегистрироваться")
        self.registration_action_button.clicked.connect(self.register_new_user)
        action_buttons_layout.addWidget(self.registration_action_button)
        
        dialog_layout.addLayout(action_buttons_layout)
        
        self.status_display_label = QLabel("")
        self.status_display_label.setStyleSheet("color: red;")
        dialog_layout.addWidget(self.status_display_label)
        
        self.setLayout(dialog_layout)
    
    def authenticate_user(self):
        username_input = self.username_input_field.text().strip()
        if not username_input:
            self.status_display_label.setText("Введите имя пользователя")
            return
        
        authentication_result, message = self.user_account_manager.authenticate_user(username_input)
        if authentication_result:
            self.accept()
        else:
            self.status_display_label.setText(message)
    
    def register_new_user(self):
        username_input = self.username_input_field.text().strip()
        if not username_input:
            self.status_display_label.setText("Введите имя пользователя")
            return
        
        registration_result, message = self.user_account_manager.register_new_user(username_input)
        if registration_result:
            self.accept()
        else:
            self.status_display_label.setText(message)