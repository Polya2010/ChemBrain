import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QLabel,
    QProgressBar,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class UserProfileInterface(QWidget):
    def __init__(self, account_manager):
        super().__init__()
        self.account_manager = account_manager
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 18pt; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(title_label)

        top_container = QHBoxLayout()

        self.avatar_container = QGroupBox("Аватарка")
        avatar_layout = QVBoxLayout()

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(150, 150)
        self.avatar_label.setStyleSheet(
            "border: 2px solid #ccc; border-radius: 5px;"
        )
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(self.avatar_label)

        avatar_buttons_layout = QHBoxLayout()

        self.change_avatar_button = QPushButton("Изменить аватарку")
        self.change_avatar_button.clicked.connect(self._change_avatar)
        avatar_buttons_layout.addWidget(self.change_avatar_button)

        self.remove_avatar_button = QPushButton("Удалить аватарку")
        self.remove_avatar_button.clicked.connect(self._remove_avatar)
        avatar_buttons_layout.addWidget(self.remove_avatar_button)

        avatar_layout.addLayout(avatar_buttons_layout)
        self.avatar_container.setLayout(avatar_layout)
        top_container.addWidget(self.avatar_container)

        user_info_group = QGroupBox("Основная информация")
        info_layout = QGridLayout()

        self.username_display = QLabel()
        self.level_display = QLabel()
        self.xp_display = QLabel()
        self.xp_progress_indicator = QProgressBar()
        self.streak_display = QLabel()
        self.quizzes_count_display = QLabel()

        info_layout.addWidget(QLabel("Имя пользователя:"), 0, 0)
        info_layout.addWidget(self.username_display, 0, 1)
        info_layout.addWidget(QLabel("Уровень:"), 1, 0)
        info_layout.addWidget(self.level_display, 1, 1)
        info_layout.addWidget(QLabel("Опыт:"), 2, 0)
        info_layout.addWidget(self.xp_display, 2, 1)
        info_layout.addWidget(QLabel("Прогресс уровня:"), 3, 0)
        info_layout.addWidget(self.xp_progress_indicator, 3, 1)
        info_layout.addWidget(QLabel("Текущая серия:"), 4, 0)
        info_layout.addWidget(self.streak_display, 4, 1)
        info_layout.addWidget(QLabel("Пройдено викторин:"), 5, 0)
        info_layout.addWidget(self.quizzes_count_display, 5, 1)

        user_info_group.setLayout(info_layout)
        top_container.addWidget(user_info_group, 1)

        layout.addLayout(top_container)

        achievements_group = QGroupBox("Достижения")
        achievements_layout = QVBoxLayout()

        self.achievements_list_widget = QListWidget()
        achievements_layout.addWidget(self.achievements_list_widget)

        achievements_group.setLayout(achievements_layout)
        layout.addWidget(achievements_group)

        self.setLayout(layout)

    def refresh_profile_data(self):
        if not self.account_manager.current_user:
            return

        current_user = self.account_manager.current_user

        self.username_display.setText(current_user.user_name)
        self.level_display.setText(f"{current_user.user_level}")
        self.xp_display.setText(f"{current_user.accumulated_experience} XP")

        current_level_xp = (
            current_user.accumulated_experience
            - ((current_user.user_level - 1) * 1000)
        )
        progress_percentage = (current_level_xp / 1000) * 100
        self.xp_progress_indicator.setValue(int(progress_percentage))

        streak_text = (
            f"{current_user.correct_streak} "
            f"(рекорд: {current_user.maximum_streak})"
        )
        self.streak_display.setText(streak_text)
        self.quizzes_count_display.setText(
            f"{len(current_user.quiz_records)}"
        )

        self._load_user_avatar(current_user.user_name)

        self.achievements_list_widget.clear()
        for achievement_record in current_user.obtained_achievements:
            item_text = (
                f"✓ {achievement_record['name']} "
                f"({achievement_record['unlock_date']})"
            )
            list_item = QListWidgetItem(item_text)
            self.achievements_list_widget.addItem(list_item)

    def _load_user_avatar(self, username):
        try:
            avatar_path = self.account_manager.get_user_avatar_path(
                username
            )
            pixmap = QPixmap(avatar_path)

            if pixmap.isNull():
                pixmap = QPixmap(150, 150)
                pixmap.fill(Qt.GlobalColor.lightGray)

            pixmap = pixmap.scaled(
                150,
                150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.avatar_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Ошибка загрузки аватарки: {e}")
            pixmap = QPixmap(150, 150)
            pixmap.fill(Qt.GlobalColor.lightGray)
            self.avatar_label.setPixmap(pixmap)

    def _change_avatar(self):
        if not self.account_manager.current_user:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Необходимо войти в систему"
            )
            return

        username = self.account_manager.current_user.user_name

        file_dialog = QFileDialog()
        file_dialog.setWindowTitle(
            "Выберите изображение для аватарки"
        )
        file_filter = "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        file_dialog.setNameFilter(file_filter)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]

                file_size = os.path.getsize(image_path)
                max_size = 5 * 1024 * 1024  # 5 МБ
                if file_size > max_size:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Файл слишком большой. Максимальный размер - 5 МБ."
                    )
                    return

                success, message = (
                    self.account_manager.save_user_avatar(
                        username,
                        image_path
                    )
                )

                if success:
                    QMessageBox.information(self, "Успех", message)
                    self._load_user_avatar(username)
                else:
                    QMessageBox.warning(self, "Ошибка", message)

    def _remove_avatar(self):
        if not self.account_manager.current_user:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Необходимо войти в систему"
            )
            return

        username = self.account_manager.current_user.user_name

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить аватарку?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = (
                self.account_manager.remove_user_avatar(username)
            )

            if success:
                QMessageBox.information(self, "Успех", message)
                self._load_user_avatar(username)
            else:
                QMessageBox.warning(self, "Ошибка", message)
