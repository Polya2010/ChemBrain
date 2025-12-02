import json
import os
from study_user import StudyUser

class UserAccountManager:
    def __init__(self):
        self.active_user = None
        self.registered_users = []
        self.available_achievements = self._initialize_achievements()
        self.load_user_data()
    
    def _get_data_path(self, filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(parent_dir, 'data')
        return os.path.join(data_dir, filename)
    
    def _initialize_achievements(self):
        return [
            {'id': 1, 'name': 'Первые шаги', 'description': 'Пройти первую викторину'},
            {'id': 2, 'name': 'Серия удач', 'description': 'Ответить правильно на 10 вопросов подряд'},
            {'id': 4, 'name': 'Эрудит', 'description': 'Набрать 100% правильных ответов в викторине'},
            {'id': 7, 'name': 'Скорострел', 'description': 'Пройти викторину менее чем за 2 минуты'},
            {'id': 10, 'name': 'Менделеев нашего времени', 'description': 'Достичь 10 уровня'},
        ]
    
    def save_user_data(self):
        data_structure = {
            'users': [user.convert_to_dictionary() for user in self.registered_users],
            'achievements': self.available_achievements
        }
        try:
            data_dir = os.path.dirname(self._get_data_path(''))
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            user_data_path = self._get_data_path('user_progress_data.json')
            with open(user_data_path, 'w', encoding='utf-8') as file:
                json.dump(data_structure, file, ensure_ascii=False, indent=2)
        except Exception as error:
            print(f"Ошибка сохранения данных: {error}")
    
    def load_user_data(self):
        try:
            user_data_path = self._get_data_path('user_progress_data.json')
            if os.path.exists(user_data_path):
                with open(user_data_path, 'r', encoding='utf-8') as file:
                    loaded_data = json.load(file)
                    self.registered_users = [StudyUser.create_from_dictionary(user_data) for user_data in loaded_data.get('users', [])]
                    self.available_achievements = loaded_data.get('achievements', self.available_achievements)
        except Exception as error:
            print(f"Ошибка загрузки данных: {error}")
    
    def register_new_user(self, username):
        if any(user.username == username for user in self.registered_users):
            return False, "Пользователь с таким именем уже существует"
        
        new_user = StudyUser(username)
        self.registered_users.append(new_user)
        self.active_user = new_user
        self.save_user_data()
        return True, f"Пользователь {username} успешно зарегистрирован"
    
    def authenticate_user(self, username):
        for user in self.registered_users:
            if user.username == username:
                self.active_user = user
                return True, f"Добро пожаловать, {username}!"
        return False, "Пользователь не найден"
    
    def user_logout(self):
        self.active_user = None
    
    def evaluate_achievement_progress(self, quiz_data):
        if not self.active_user:
            return []
        
        newly_unlocked = []
        
        if len(self.active_user.quiz_history_log) == 1:
            achievement = self.get_achievement_by_id(1)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if self.active_user.correct_answer_streak >= 10:
            achievement = self.get_achievement_by_id(2)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if quiz_data['correct_answers'] == quiz_data['total_questions']:
            achievement = self.get_achievement_by_id(4)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if quiz_data['time_spent_seconds'] < 120:
            achievement = self.get_achievement_by_id(7)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if self.active_user.current_level >= 10:
            achievement = self.get_achievement_by_id(10)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if newly_unlocked:
            self.save_user_data()
        
        return newly_unlocked
    
    def get_achievement_by_id(self, achievement_id):
        for achievement in self.available_achievements:
            if achievement['id'] == achievement_id:
                return achievement
        return None