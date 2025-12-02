import random
from PyQt6.QtCore import QDateTime, Qt

class StudyUser:
    def __init__(self, username, user_identifier=None):
        self.user_identifier = user_identifier or random.randint(1000, 9999)
        self.username = username
        self.current_level = 1
        self.total_experience = 0
        self.account_creation_date = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        self.unlocked_achievements = []
        self.quiz_history_log = []
        self.correct_answer_streak = 0
        self.max_correct_streak = 0
    
    def add_experience_points(self, experience_points):
        self.total_experience += int(experience_points)
        required_experience = self.current_level * 1000
        if self.total_experience >= required_experience:
            self.current_level += 1
            return True
        return False
    
    def unlock_achievement(self, achievement_data):
        if achievement_data not in self.unlocked_achievements:
            self.unlocked_achievements.append({
                'id': achievement_data['id'],
                'name': achievement_data['name'],
                'unlock_date': QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
            })
            return True
        return False
    
    def record_quiz_result(self, quiz_result_data):
        self.quiz_history_log.append(quiz_result_data)
    
    def update_answer_streak(self, was_correct):
        if was_correct:
            self.correct_answer_streak += 1
            self.max_correct_streak = max(self.max_correct_streak, self.correct_answer_streak)
        else:
            self.correct_answer_streak = 0
    
    def convert_to_dictionary(self):
        return {
            'user_identifier': self.user_identifier,
            'username': self.username,
            'current_level': self.current_level,
            'total_experience': self.total_experience,
            'account_creation_date': self.account_creation_date,
            'unlocked_achievements': self.unlocked_achievements,
            'quiz_history_log': self.quiz_history_log,
            'correct_answer_streak': self.correct_answer_streak,
            'max_correct_streak': self.max_correct_streak
        }
    
    @classmethod
    def create_from_dictionary(cls, data_dict):
        user_instance = cls(data_dict['username'], data_dict['user_identifier'])
        user_instance.current_level = data_dict['current_level']
        user_instance.total_experience = data_dict['total_experience']
        user_instance.account_creation_date = data_dict['account_creation_date']
        user_instance.unlocked_achievements = data_dict.get('unlocked_achievements', [])
        user_instance.quiz_history_log = data_dict.get('quiz_history_log', [])
        user_instance.correct_answer_streak = data_dict.get('correct_answer_streak', 0)
        user_instance.max_correct_streak = data_dict.get('max_correct_streak', 0)
        return user_instance