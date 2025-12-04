import os
import sqlite3
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt
from database_manager import DatabaseManager
from modified_study_user import LearningUser


class AccountManager:
    def __init__(self):
        self.current_user = None
        self.db_manager = DatabaseManager()
        self._init_achievements()
        self.avatars_directory = self._get_avatars_directory()
    
    def _get_avatars_directory(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        data_directory = os.path.join(parent_directory, 'data')
        avatars_directory = os.path.join(data_directory, 'avatars')
        
        if not os.path.exists(avatars_directory):
            os.makedirs(avatars_directory)
        
        return avatars_directory
    
    def _init_achievements(self):
        achievements = [
            ('Начало пути', 'Пройти первую викторину', 10),
            ('Последовательность успеха', 'Ответить правильно на 10 вопросов подряд', 20),
            ('Знаток химии', 'Набрать 100% правильных ответов в викторине', 30),
            ('Молниеносный ответ', 'Пройти викторину менее чем за 2 минуты', 25),
            ('Современный Менделеев', 'Достичь 10 уровня', 50),
        ]
        
        for name, description, points in achievements:
            self.db_manager.add_achievement(name, description, points)
    
    def create_new_account(self, username):
        existing_user = self.db_manager.get_user(username)
        if existing_user:
            return False, "Пользователь с таким именем уже зарегистрирован"
        
        user_id = self.db_manager.add_user(username)
        if user_id:
            user_data = self.db_manager.get_user(username)
            if user_data:
                self.current_user = LearningUser(user_data)
            return True, f"Пользователь {username} успешно создан"
        return False, "Ошибка создания пользователя"
    
    def verify_user(self, username):
        user_data = self.db_manager.get_user(username)
        if user_data:
            self.current_user = LearningUser(user_data)
            return True, f"Приветствуем, {username}!"
        return False, "Пользователь не найден"
    
    def user_logout(self):
        self.current_user = None
    
    def add_experience(self, experience_amount):
        if not self.current_user:
            return False
        
        level_increased = self.current_user.add_experience(experience_amount)
        
        if self.current_user:
            user_data = self.db_manager.get_user_by_id(self.current_user.user_id)
            if user_data:
                self.current_user = LearningUser(user_data)
        
        return level_increased
    
    def update_streak_counter(self, answer_correct):
        if not self.current_user:
            return
        
        self.current_user.update_streak_counter(answer_correct)
    
    def save_quiz_result(self, quiz_result_record):
        if not self.current_user:
            return False
        
        return self.current_user.save_quiz_result(quiz_result_record)
    
    def check_achievement_progress(self, quiz_results):
        if not self.current_user:
            return []
        
        newly_obtained = []
        user_id = self.current_user.user_id
        
        achievements = self.db_manager.get_all_achievements()
        
        quiz_history = self.db_manager.get_user_quiz_history(user_id, 1)
        if len(quiz_history) == 1:
            first_achievement = next((a for a in achievements if a['name'] == 'Начало пути'), None)
            if first_achievement and self.db_manager.unlock_achievement(user_id, first_achievement['achievement_id']):
                newly_obtained.append(first_achievement)
        
        if self.current_user.correct_streak >= 10:
            streak_achievement = next((a for a in achievements if a['name'] == 'Последовательность успеха'), None)
            if streak_achievement and self.db_manager.unlock_achievement(user_id, streak_achievement['achievement_id']):
                newly_obtained.append(streak_achievement)
        
        if quiz_results.get('correct_responses', 0) == quiz_results.get('total_questions', 0) and quiz_results.get('total_questions', 0) > 0:
            perfect_achievement = next((a for a in achievements if a['name'] == 'Знаток химии'), None)
            if perfect_achievement and self.db_manager.unlock_achievement(user_id, perfect_achievement['achievement_id']):
                newly_obtained.append(perfect_achievement)
        
        if quiz_results.get('time_elapsed_seconds', 0) < 120:
            speed_achievement = next((a for a in achievements if a['name'] == 'Молниеносный ответ'), None)
            if speed_achievement and self.db_manager.unlock_achievement(user_id, speed_achievement['achievement_id']):
                newly_obtained.append(speed_achievement)
        
        if self.current_user.user_level >= 10:
            level_achievement = next((a for a in achievements if a['name'] == 'Современный Менделеев'), None)
            if level_achievement and self.db_manager.unlock_achievement(user_id, level_achievement['achievement_id']):
                newly_obtained.append(level_achievement)
        
        return newly_obtained
    
    def get_user_achievements(self):
        if not self.current_user:
            return []
        
        return self.db_manager.get_user_achievements(self.current_user.user_id)
    
    def get_user_quiz_history(self, limit=10):
        if not self.current_user:
            return []
        
        return self.db_manager.get_user_quiz_history(self.current_user.user_id, limit)
    
    def get_user_avatar_path(self, username):
        avatar_filename = f"{username}_avatar.png"
        avatar_path = os.path.join(self.avatars_directory, avatar_filename)
        
        if os.path.exists(avatar_path):
            return avatar_path
        
        default_avatar_path = os.path.join(self.avatars_directory, "default_avatar.png")
        if not os.path.exists(default_avatar_path):
            self._create_default_avatar(default_avatar_path)
        
        return default_avatar_path
    
    def _create_default_avatar(self, path):
        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor(200, 220, 240))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor(100, 150, 200))
        painter.setBrush(QColor(100, 150, 200))
        painter.drawEllipse(10, 10, 80, 80)
        
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 40))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "?")
        painter.end()
        
        pixmap.save(path)
    
    def save_user_avatar(self, username, image_path):
        try:
            import shutil
            avatar_filename = f"{username}_avatar.png"
            destination_path = os.path.join(self.avatars_directory, avatar_filename)
            
            shutil.copy2(image_path, destination_path)
            
            if self.current_user and self.current_user.user_name == username:
                self.current_user.set_avatar_filename(avatar_filename)
            
            return True, "Аватарка успешно сохранена"
        except Exception as e:
            return False, f"Ошибка сохранения аватарки: {str(e)}"
    
    def remove_user_avatar(self, username):
        try:
            avatar_filename = f"{username}_avatar.png"
            avatar_path = os.path.join(self.avatars_directory, avatar_filename)
            
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
                return True, "Аватарка удалена"
            return True, "Аватарка не существует"
        except Exception as e:
            return False, f"Ошибка удаления аватарки: {str(e)}"