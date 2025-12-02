from PyQt6.QtCore import QDateTime, Qt

class QuizSession:
    def __init__(self, name, questions, user_manager):
        self.name = name
        self.questions = questions
        self.user_manager = user_manager
        self.current_index = 0
        self.score = 0
        self.total = len(questions) if questions else 0
        self.start_time = QDateTime.currentDateTime()
        self.answers = []
        self.done = False
        self.xp_earned = 0
    
    def get_current_question(self):
        if self.current_index < self.total and self.questions:
            return self.questions[self.current_index]
        return None
    
    def submit_answer(self, answer):
        try:
            current = self.get_current_question()
            if not current:
                self.done = True
                return False
            
            correct = current.validate_answer(answer)
            
            if self.user_manager.active_user:
                self.user_manager.active_user.update_answer_streak(correct)
            
            if correct:
                self.score += current.point_value
                xp_for_answer = current.point_value * 10
                self.xp_earned += xp_for_answer
            else:
                xp_for_answer = 0
            
            self.answers.append({
                'question': current.question_text,
                'user_answer': answer,
                'correct': current.correct_answer,
                'is_correct': correct,
                'points': current.point_value if correct else 0,
                'xp_earned': xp_for_answer if correct else 0
            })
            
            self.current_index += 1
            
            if self.current_index >= self.total:
                self.done = True
                return self._finalize_quiz_session()
            
            return correct
        except Exception as e:
            print(f"Ошибка при отправке ответа: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _finalize_quiz_session(self):
        try:
            if not self.user_manager or not self.user_manager.active_user:
                print("Пользователь не авторизован")
                return None, [], False
            
            print("Начинаем финализацию викторины...")
            
            completion_xp = len(self.questions) * 5 if self.questions else 0
            self.xp_earned += completion_xp
            
            time_elapsed = self.start_time.secsTo(QDateTime.currentDateTime())
            print(f"Время викторины: {time_elapsed} секунд")
            
            if time_elapsed < 300:
                speed_bonus = 50
                self.xp_earned += speed_bonus
                print(f"Бонус за скорость: +{speed_bonus} XP")
            
            total_possible_points = sum(q.point_value for q in self.questions) if self.questions else 0
            accuracy = self.score / total_possible_points if total_possible_points > 0 else 0
            if accuracy >= 0.8:
                accuracy_bonus = int(100 * accuracy)
                self.xp_earned += accuracy_bonus
                print(f"Бонус за точность: +{accuracy_bonus} XP")
            
            print(f"Всего получено XP: {self.xp_earned}")
            
            level_up = self.user_manager.active_user.add_experience_points(int(self.xp_earned))
            
            quiz_data = {
                'timestamp': QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate),
                'quiz_name': self.name,
                'total_questions': self.total,
                'correct_answers': sum(1 for a in self.answers if a['is_correct']) if self.answers else 0,
                'score': self.score,
                'max_score': total_possible_points,
                'time_spent_seconds': int(time_elapsed),
                'xp_earned': int(self.xp_earned),
                'level_up': level_up
            }
            
            print(f"Данные викторины: {quiz_data}")
            
            self.user_manager.active_user.record_quiz_result(quiz_data)
            
            achievements_unlocked = self.user_manager.evaluate_achievement_progress(quiz_data)
            quiz_data['achievements_unlocked'] = [a['name'] for a in achievements_unlocked]
            
            print(f"Разблокировано достижений: {len(achievements_unlocked)}")
            
            self.user_manager.save_user_data()
            
            print("Викторина успешно завершена")
            return quiz_data, achievements_unlocked, level_up
            
        except Exception as e:
            print(f"Ошибка при финализации викторины: {e}")
            import traceback
            traceback.print_exc()
            return None, [], False
    
    def get_progress_percentage(self):
        return (self.current_index / self.total) * 100 if self.total > 0 else 0
    
    def get_elapsed_time(self):
        return self.start_time.secsTo(QDateTime.currentDateTime())