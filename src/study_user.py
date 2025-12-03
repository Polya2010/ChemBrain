import random
from PyQt6.QtCore import QDateTime, Qt


class LearningUser:
    def __init__(self, user_name, user_id=None):
        self.user_id = user_id or random.randint(1000, 9999)
        self.user_name = user_name
        self.user_level = 1
        self.accumulated_experience = 0
        self.registration_date = QDateTime.currentDateTime().toString(
            Qt.DateFormat.ISODate
        )
        self.obtained_achievements = []
        self.quiz_records = []
        self.correct_streak = 0
        self.maximum_streak = 0
        self.avatar_filename = None

    def add_experience(self, experience_amount):
        self.accumulated_experience += int(experience_amount)
        required_experience = self.user_level * 1000
        if self.accumulated_experience >= required_experience:
            self.user_level += 1
            return True
        return False

    def unlock_achievement_record(self, achievement_record):
        if achievement_record not in self.obtained_achievements:
            self.obtained_achievements.append({
                'id': achievement_record['id'],
                'name': achievement_record['name'],
                'unlock_date': QDateTime.currentDateTime().toString(
                    Qt.DateFormat.ISODate
                )
            })
            return True
        return False

    def save_quiz_result(self, quiz_result_record):
        self.quiz_records.append(quiz_result_record)

    def update_streak_counter(self, answer_correct):
        if answer_correct:
            self.correct_streak += 1
            self.maximum_streak = max(
                self.maximum_streak,
                self.correct_streak
            )
        else:
            self.correct_streak = 0

    def to_dict_format(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_level': self.user_level,
            'accumulated_experience': self.accumulated_experience,
            'registration_date': self.registration_date,
            'obtained_achievements': self.obtained_achievements,
            'quiz_records': self.quiz_records,
            'correct_streak': self.correct_streak,
            'maximum_streak': self.maximum_streak,
            'avatar_filename': self.avatar_filename
        }

    @classmethod
    def from_dict_format(cls, data_dict):
        user_instance = cls(
            data_dict['user_name'],
            data_dict['user_id']
        )
        user_instance.user_level = data_dict['user_level']
        user_instance.accumulated_experience = (
            data_dict['accumulated_experience']
        )
        user_instance.registration_date = data_dict['registration_date']
        user_instance.obtained_achievements = (
            data_dict.get('obtained_achievements', [])
        )
        user_instance.quiz_records = data_dict.get('quiz_records', [])
        user_instance.correct_streak = data_dict.get('correct_streak', 0)
        user_instance.maximum_streak = data_dict.get('maximum_streak', 0)
        user_instance.avatar_filename = data_dict.get(
            'avatar_filename',
            None
        )
        return user_instance

    def set_avatar_filename(self, filename):
        self.avatar_filename = filename

    def get_avatar_filename(self):
        return self.avatar_filename
