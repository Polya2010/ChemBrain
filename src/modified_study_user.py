from database_manager import DatabaseManager


class LearningUser:
    def __init__(self, user_data):
        self.user_id = user_data['user_id']
        self.user_name = user_data['username']
        self.user_level = user_data['user_level']
        self.accumulated_experience = user_data['accumulated_experience']
        self.registration_date = user_data['registration_date']
        self.correct_streak = user_data['correct_streak']
        self.maximum_streak = user_data['maximum_streak']
        self.avatar_filename = user_data.get('avatar_filename')
        self.db_manager = DatabaseManager()
    
    def add_experience(self, experience_amount):
        success = self.db_manager.update_user_experience(self.user_id, experience_amount)
        if success:
            self.accumulated_experience += experience_amount
            
            required_experience = self.user_level * 1000
            if self.accumulated_experience >= required_experience:
                new_level = self.user_level + 1
                level_success = self.db_manager.update_user_level(self.user_id, new_level)
                if level_success:
                    self.user_level = new_level
                    return True
        return False
    
    def update_streak_counter(self, answer_correct):
        self.db_manager.update_user_streak(self.user_id, answer_correct)
        if answer_correct:
            self.correct_streak += 1
            self.maximum_streak = max(self.maximum_streak, self.correct_streak)
        else:
            self.correct_streak = 0
    
    def save_quiz_result(self, quiz_result_record):
        return self.db_manager.save_quiz_result(self.user_id, quiz_result_record)
    
    def get_achievements(self):
        return self.db_manager.get_user_achievements(self.user_id)
    
    def get_quiz_history(self, limit=10):
        return self.db_manager.get_user_quiz_history(self.user_id, limit)
    
    def set_avatar_filename(self, filename):
        self.avatar_filename = filename
    
    def get_avatar_filename(self):
        return self.avatar_filename
    
    def to_dict(self):
        """Преобразует объект в словарь"""
        return {
            'user_id': self.user_id,
            'username': self.user_name,
            'user_level': self.user_level,
            'accumulated_experience': self.accumulated_experience,
            'registration_date': self.registration_date,
            'correct_streak': self.correct_streak,
            'maximum_streak': self.maximum_streak,
            'avatar_filename': self.avatar_filename
        }