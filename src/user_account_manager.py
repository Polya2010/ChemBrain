import json
import os
import base64
from PyQt6.QtGui import QPixmap
from study_user import LearningUser


class AccountManager:
    def __init__(self):
        self.current_user = None
        self.user_registry = []
        self.available_achievements = self._create_achievements_list()
        self.avatars_directory = self._get_avatars_directory()
        self.load_saved_data()

    def _get_avatars_directory(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        data_directory = os.path.join(parent_directory, 'data')
        avatars_directory = os.path.join(data_directory, 'avatars')

        if not os.path.exists(avatars_directory):
            os.makedirs(avatars_directory)

        return avatars_directory

    def _get_file_path(self, filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        data_directory = os.path.join(parent_directory, 'data')
        return os.path.join(data_directory, filename)

    def _create_achievements_list(self):
        return [
            {
                'id': 1,
                'name': 'Начало пути',
                'description': 'Пройти первую викторину'
            },
            {
                'id': 2,
                'name': 'Последовательность успеха',
                'description': 'Ответить правильно на 10 вопросов подряд'
            },
            {
                'id': 4,
                'name': 'Знаток химии',
                'description': 'Набрать 100% правильных ответов в викторине'
            },
            {
                'id': 7,
                'name': 'Молниеносный ответ',
                'description': 'Пройти викторину менее чем за 2 минуты'
            },
            {
                'id': 10,
                'name': 'Современный Менделеев',
                'description': 'Достичь 10 уровня'
            },
        ]

    def save_user_data(self):
        data_structure = {
            'users': [
                user.to_dict_format() for user in self.user_registry
            ],
            'achievements': self.available_achievements
        }
        try:
            data_directory = os.path.dirname(self._get_file_path(''))
            if not os.path.exists(data_directory):
                os.makedirs(data_directory)

            user_data_file = self._get_file_path('user_progress_data.json')
            file_mode = 'w'
            encoding = 'utf-8'
            with open(user_data_file, file_mode, encoding=encoding) as fh:
                json.dump(
                    data_structure,
                    fh,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception as error:
            print(f"Ошибка сохранения данных: {error}")

    def load_saved_data(self):
        try:
            user_data_file = self._get_file_path('user_progress_data.json')
            if os.path.exists(user_data_file):
                file_mode = 'r'
                encoding = 'utf-8'
                with open(user_data_file, file_mode, encoding=encoding) as fh:
                    loaded_data = json.load(fh)
                    self.user_registry = [
                        LearningUser.from_dict_format(user_data)
                        for user_data in loaded_data.get('users', [])
                    ]
                    self.available_achievements = loaded_data.get(
                        'achievements',
                        self.available_achievements
                    )
        except Exception as error:
            print(f"Ошибка загрузки данных: {error}")

    def create_new_account(self, username):
        user_exists = any(
            user.user_name == username
            for user in self.user_registry
        )
        if user_exists:
            return False, "Пользователь с таким именем уже зарегистрирован"

        new_user_account = LearningUser(username)
        self.user_registry.append(new_user_account)
        self.current_user = new_user_account
        self.save_user_data()
        return True, f"Пользователь {username} успешно создан"

    def verify_user(self, username):
        for user_account in self.user_registry:
            if user_account.user_name == username:
                self.current_user = user_account
                return True, f"Приветствуем, {username}!"
        return False, "Пользователь не найден"

    def user_logout(self):
        self.current_user = None

    def check_achievement_progress(self, quiz_results):
        if not self.current_user:
            return []

        newly_obtained = []

        if len(self.current_user.quiz_records) == 1:
            achievement_item = self.get_achievement_by_id(1)
            if self.current_user.unlock_achievement_record(achievement_item):
                newly_obtained.append(achievement_item)

        if self.current_user.correct_streak >= 10:
            achievement_item = self.get_achievement_by_id(2)
            if self.current_user.unlock_achievement_record(achievement_item):
                newly_obtained.append(achievement_item)

        correct_equals_total = (
            quiz_results['correct_responses']
            == quiz_results['total_questions']
        )
        if correct_equals_total:
            achievement_item = self.get_achievement_by_id(4)
            if self.current_user.unlock_achievement_record(achievement_item):
                newly_obtained.append(achievement_item)

        if quiz_results['time_elapsed_seconds'] < 120:
            achievement_item = self.get_achievement_by_id(7)
            if self.current_user.unlock_achievement_record(achievement_item):
                newly_obtained.append(achievement_item)

        if self.current_user.user_level >= 10:
            achievement_item = self.get_achievement_by_id(10)
            if self.current_user.unlock_achievement_record(achievement_item):
                newly_obtained.append(achievement_item)

        if newly_obtained:
            self.save_user_data()

        return newly_obtained

    def get_achievement_by_id(self, achievement_id):
        for achievement_item in self.available_achievements:
            if achievement_item['id'] == achievement_id:
                return achievement_item
        return None

    def get_user_avatar_path(self, username):
        avatar_filename = f"{username}_avatar.png"
        avatar_path = os.path.join(self.avatars_directory, avatar_filename)

        if os.path.exists(avatar_path):
            return avatar_path

        default_avatar_path = os.path.join(
            self.avatars_directory,
            "default_avatar.png"
        )
        if not os.path.exists(default_avatar_path):
            self._create_default_avatar(default_avatar_path)

        return default_avatar_path

    def _create_default_avatar(self, path):
        from PyQt6.QtGui import QPainter, QColor, QFont
        from PyQt6.QtCore import Qt

        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor(200, 220, 240))

        painter = QPainter(pixmap)
        painter.setPen(QColor(100, 150, 200))
        painter.setBrush(QColor(100, 150, 200))
        painter.drawEllipse(10, 10, 80, 80)

        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 40))
        painter.drawText(
            pixmap.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "?"
        )
        painter.end()

        pixmap.save(path)

    def save_user_avatar(self, username, image_path):
        try:
            import shutil
            avatar_filename = f"{username}_avatar.png"
            destination_path = os.path.join(
                self.avatars_directory,
                avatar_filename
            )

            shutil.copy2(image_path, destination_path)
            return True, "Аватарка успешно сохранена"
        except Exception as e:
            return False, f"Ошибка сохранения аватарки: {str(e)}"

    def remove_user_avatar(self, username):
        try:
            avatar_filename = f"{username}_avatar.png"
            avatar_path = os.path.join(
                self.avatars_directory,
                avatar_filename
            )

            if os.path.exists(avatar_path):
                os.remove(avatar_path)
                return True, "Аватарка удалена"
            return True, "Аватарка не существует"
        except Exception as e:
            return False, f"Ошибка удаления аватарки: {str(e)}"
