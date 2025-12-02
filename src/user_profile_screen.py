from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QGridLayout, 
    QLabel, QProgressBar, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

class UserProfileScreen(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_account_manager = user_manager
        self.setup_interface()
    
    def setup_interface(self):
        layout = QVBoxLayout()
        
        title = QLabel("ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (Ctrl+S)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        info_group = QGroupBox("Основная информация")
        info_layout = QGridLayout()
        
        self.username_label = QLabel()
        self.level_label = QLabel()
        self.xp_label = QLabel()
        self.xp_progress = QProgressBar()
        self.streak_label = QLabel()
        self.quizzes_label = QLabel()
        
        info_layout.addWidget(QLabel("Имя пользователя:"), 0, 0)
        info_layout.addWidget(self.username_label, 0, 1)
        info_layout.addWidget(QLabel("Уровень:"), 1, 0)
        info_layout.addWidget(self.level_label, 1, 1)
        info_layout.addWidget(QLabel("Опыт:"), 2, 0)
        info_layout.addWidget(self.xp_label, 2, 1)
        info_layout.addWidget(QLabel("Прогресс уровня:"), 3, 0)
        info_layout.addWidget(self.xp_progress, 3, 1)
        info_layout.addWidget(QLabel("Текущая серия:"), 4, 0)
        info_layout.addWidget(self.streak_label, 4, 1)
        info_layout.addWidget(QLabel("Пройдено викторин:"), 5, 0)
        info_layout.addWidget(self.quizzes_label, 5, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        achievements_group = QGroupBox("Достижения")
        achievements_layout = QVBoxLayout()
        
        self.achievements_list = QListWidget()
        achievements_layout.addWidget(self.achievements_list)
        
        achievements_group.setLayout(achievements_layout)
        layout.addWidget(achievements_group)
        
        buttons_layout = QHBoxLayout()
        
        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.clicked.connect(self.logout_user)
        buttons_layout.addWidget(self.logout_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def update_profile_display(self):
        if not self.user_account_manager.active_user:
            return
        
        user = self.user_account_manager.active_user
        
        self.username_label.setText(user.username)
        self.level_label.setText(f"{user.current_level}")
        self.xp_label.setText(f"{user.total_experience} XP")
        
        current_level_xp = user.total_experience - ((user.current_level - 1) * 1000)
        progress = (current_level_xp / 1000) * 100
        self.xp_progress.setValue(int(progress))
        
        self.streak_label.setText(f"{user.correct_answer_streak} (макс: {user.max_correct_streak})")
        self.quizzes_label.setText(f"{len(user.quiz_history_log)}")
        
        self.achievements_list.clear()
        for achievement in user.unlocked_achievements:
            item = QListWidgetItem(f"✓ {achievement['name']} ({achievement['unlock_date']})")
            self.achievements_list.addItem(item)
    
    def logout_user(self):
        self.user_account_manager.user_logout()
        self.parent().display_authentication_dialog()