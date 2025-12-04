from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
    QFileDialog, QMessageBox, QProgressBar
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os


class UserProfileInterface(QWidget):
    def __init__(self, account_manager):
        super().__init__()
        self.account_manager = account_manager
        self._initialize_interface()

    def _initialize_interface(self):
        layout = QVBoxLayout()
        
        self.profile_header = QLabel("ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ")
        self.profile_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_header.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
        layout.addWidget(self.profile_header)
        
        self.profile_container = QWidget()
        self.profile_layout = QVBoxLayout()
        
        self.user_info_section = self._create_user_info_section()
        self.profile_layout.addWidget(self.user_info_section)
        
        self.avatar_section = self._create_avatar_section()
        self.profile_layout.addWidget(self.avatar_section)
        
        self.achievements_section = self._create_achievements_section()
        self.profile_layout.addWidget(self.achievements_section)
        
        self.quiz_history_section = self._create_quiz_history_section()
        self.profile_layout.addWidget(self.quiz_history_section)
        
        self.profile_container.setLayout(self.profile_layout)
        layout.addWidget(self.profile_container)
        
        self.setLayout(layout)

    def _create_user_info_section(self):
        section = QGroupBox("Информация о пользователе")
        layout = QVBoxLayout()
        
        self.username_label = QLabel("Имя пользователя: ")
        self.user_level_label = QLabel("Уровень: ")
        self.user_xp_label = QLabel("Опыт: ")
        self.registration_label = QLabel("Дата регистрации: ")
        self.streak_label = QLabel("Текущая серия правильных ответов: ")
        self.max_streak_label = QLabel("Максимальная серия: ")
        
        layout.addWidget(self.username_label)
        layout.addWidget(self.user_level_label)
        layout.addWidget(self.user_xp_label)
        layout.addWidget(self.registration_label)
        layout.addWidget(self.streak_label)
        layout.addWidget(self.max_streak_label)
        
        section.setLayout(layout)
        return section

    def _create_avatar_section(self):
        section = QGroupBox("Аватарка")
        layout = QVBoxLayout()
        
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setFixedSize(150, 150)
        self.avatar_label.setStyleSheet("border: 2px solid #ccc; border-radius: 75px;")
        
        button_layout = QHBoxLayout()
        self.change_avatar_button = QPushButton("Изменить аватар")
        self.change_avatar_button.clicked.connect(self._change_avatar)
        self.remove_avatar_button = QPushButton("Удалить аватар")
        self.remove_avatar_button.clicked.connect(self._remove_avatar)
        
        button_layout.addWidget(self.change_avatar_button)
        button_layout.addWidget(self.remove_avatar_button)
        
        layout.addWidget(self.avatar_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_layout)
        
        section.setLayout(layout)
        return section

    def _create_achievements_section(self):
        section = QGroupBox("Достижения")
        layout = QVBoxLayout()
        
        self.achievements_table = QTableWidget()
        self.achievements_table.setColumnCount(3)
        self.achievements_table.setHorizontalHeaderLabels(["Название", "Описание", "Дата получения"])
        self.achievements_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.achievements_table.setMaximumHeight(200)
        
        layout.addWidget(self.achievements_table)
        section.setLayout(layout)
        return section

    def _create_quiz_history_section(self):
        section = QGroupBox("История викторин")
        layout = QVBoxLayout()
        
        self.quiz_history_table = QTableWidget()
        self.quiz_history_table.setColumnCount(7)
        self.quiz_history_table.setHorizontalHeaderLabels([
            "Дата", "Название", "Вопросы", "Правильно", 
            "Баллы", "Время (сек)", "Опыт"
        ])
        self.quiz_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.quiz_history_table.setMaximumHeight(250)
        
        layout.addWidget(self.quiz_history_table)
        section.setLayout(layout)
        return section

    def refresh_profile_data(self):
        if not self.account_manager.current_user:
            self._clear_profile_data()
            return
        
        user = self.account_manager.current_user
        
        self.username_label.setText(f"Имя пользователя: {user.user_name}")
        self.user_level_label.setText(f"Уровень: {user.user_level}")
        self.user_xp_label.setText(f"Опыт: {user.accumulated_experience}")
        self.registration_label.setText(f"Дата регистрации: {user.registration_date}")
        self.streak_label.setText(f"Текущая серия правильных ответов: {user.correct_streak}")
        self.max_streak_label.setText(f"Максимальная серия: {user.maximum_streak}")
        
        # Исправленный путь к аватару
        try:
            avatar_path = self.account_manager.get_user_avatar_path(user.user_name)
            if os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path)
                pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.avatar_label.setPixmap(pixmap)
            else:
                self.avatar_label.clear()
                self.avatar_label.setText("Аватар\nне выбран")
                self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print(f"Ошибка загрузки аватара: {e}")
            self.avatar_label.clear()
            self.avatar_label.setText("Ошибка\nзагрузки")
            self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self._load_achievements()
        self._load_quiz_history()

    def _clear_profile_data(self):
        self.username_label.setText("Имя пользователя: ")
        self.user_level_label.setText("Уровень: ")
        self.user_xp_label.setText("Опыт: ")
        self.registration_label.setText("Дата регистрации: ")
        self.streak_label.setText("Текущая серия правильных ответов: ")
        self.max_streak_label.setText("Максимальная серия: ")
        
        self.avatar_label.clear()
        self.avatar_label.setText("Аватар\nне выбран")
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.achievements_table.setRowCount(0)
        self.quiz_history_table.setRowCount(0)

    def _load_achievements(self):
        achievements = self.account_manager.get_user_achievements()
        self.achievements_table.setRowCount(len(achievements))
        
        for row, achievement in enumerate(achievements):
            self.achievements_table.setItem(row, 0, QTableWidgetItem(achievement['name']))
            self.achievements_table.setItem(row, 1, QTableWidgetItem(achievement['description']))
            self.achievements_table.setItem(row, 2, QTableWidgetItem(achievement['unlock_date']))

    def _load_quiz_history(self):
        quiz_history = self.account_manager.get_user_quiz_history(10)
        self.quiz_history_table.setRowCount(len(quiz_history))
        
        for row, quiz in enumerate(quiz_history):
            self.quiz_history_table.setItem(row, 0, QTableWidgetItem(quiz['completed_date']))
            self.quiz_history_table.setItem(row, 1, QTableWidgetItem(quiz['quiz_title']))
            self.quiz_history_table.setItem(row, 2, QTableWidgetItem(str(quiz['total_questions'])))
            self.quiz_history_table.setItem(row, 3, QTableWidgetItem(str(quiz['correct_responses'])))
            self.quiz_history_table.setItem(row, 4, QTableWidgetItem(f"{quiz['final_score']}/{quiz['maximum_score']}"))
            self.quiz_history_table.setItem(row, 5, QTableWidgetItem(str(quiz['time_elapsed_seconds'])))
            self.quiz_history_table.setItem(row, 6, QTableWidgetItem(str(quiz['experience_earned'])))

    def _change_avatar(self):
        if not self.account_manager.current_user:
            QMessageBox.warning(self, "Ошибка", "Сначала войдите в систему")
            return
        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            username = self.account_manager.current_user.user_name
            success, message = self.account_manager.save_user_avatar(username, file_path)
            
            if success:
                QMessageBox.information(self, "Успех", message)
                self.refresh_profile_data()
            else:
                QMessageBox.warning(self, "Ошибка", message)

    def _remove_avatar(self):
        if not self.account_manager.current_user:
            QMessageBox.warning(self, "Ошибка", "Сначала войдите в систему")
            return
        
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить аватарку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            username = self.account_manager.current_user.user_name
            success, message = self.account_manager.remove_user_avatar(username)
            
            if success:
                QMessageBox.information(self, "Успех", message)
                self.refresh_profile_data()
            else:
                QMessageBox.warning(self, "Ошибка", message)