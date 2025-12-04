from PyQt6.QtCore import QDateTime, Qt


class QuizAttempt:
    def __init__(self, quiz_name, question_set, account_handler):
        self.quiz_name = quiz_name
        self.question_set = question_set
        self.account_handler = account_handler
        self.current_question_index = 0
        self.total_score = 0
        self.question_count = len(question_set) if question_set else 0
        self.attempt_start_time = QDateTime.currentDateTime()
        self.answer_records = []
        self.completed = False
        self.experience_gained = 0

    def get_active_question(self):
        if self.current_question_index < self.question_count:
            if self.question_set:
                return self.question_set[self.current_question_index]
        return None

    def process_user_response(self, user_answer):
        try:
            active_question = self.get_active_question()
            if not active_question:
                self.completed = True
                return False

            is_correct = active_question.check_answer(user_answer)

            if self.account_handler.current_user:
                self.account_handler.update_streak_counter(
                    is_correct
                )

            if is_correct:
                self.total_score += active_question.score_value
                experience_for_answer = active_question.score_value * 10
                self.experience_gained += experience_for_answer
            else:
                experience_for_answer = 0

            self.answer_records.append({
                'question_content': active_question.question_text,
                'user_response': user_answer,
                'correct_response': active_question.correct_response,
                'answer_correct': is_correct,
                'points_awarded': (
                    active_question.score_value if is_correct else 0
                ),
                'experience_awarded': (
                    experience_for_answer if is_correct else 0
                )
            })

            self.current_question_index += 1

            if self.current_question_index >= self.question_count:
                self.completed = True
                return self._finalize_quiz_attempt()

            return is_correct
        except Exception as error:
            print(f"Ошибка обработки ответа: {error}")
            import traceback
            traceback.print_exc()
            return False

    def _finalize_quiz_attempt(self):
        try:
            if not self.account_handler:
                print("Обработчик аккаунта отсутствует")
                return None, [], False
            if not self.account_handler.current_user:
                print("Пользователь не авторизован")
                return None, [], False

            print("Начало финализации викторины...")

            completion_bonus = (
                len(self.question_set) * 5 if self.question_set else 0
            )
            self.experience_gained += completion_bonus

            elapsed_time_seconds = self.attempt_start_time.secsTo(
                QDateTime.currentDateTime()
            )
            print(f"Время выполнения: {elapsed_time_seconds} секунд")

            if elapsed_time_seconds < 300:
                speed_reward = 50
                self.experience_gained += speed_reward
                print(f"Бонус за скорость: +{speed_reward} XP")

            maximum_possible_score = 0
            if self.question_set:
                maximum_possible_score = sum(
                    q.score_value for q in self.question_set
                )

            accuracy_ratio = 0
            if maximum_possible_score > 0:
                accuracy_ratio = self.total_score / maximum_possible_score

            if accuracy_ratio >= 0.8:
                accuracy_bonus = int(100 * accuracy_ratio)
                self.experience_gained += accuracy_bonus
                print(f"Бонус за точность: +{accuracy_bonus} XP")

            print(f"Общий полученный опыт: {self.experience_gained}")

            level_increased = (
                self.account_handler.add_experience(
                    int(self.experience_gained)
                )
            )

            correct_responses_count = 0
            if self.answer_records:
                correct_responses_count = sum(
                    1 for response in self.answer_records
                    if response['answer_correct']
                )

            quiz_summary = {
                'timestamp': QDateTime.currentDateTime().toString(
                    Qt.DateFormat.ISODate
                ),
                'quiz_title': self.quiz_name,
                'total_questions': self.question_count,
                'correct_responses': correct_responses_count,
                'final_score': self.total_score,
                'maximum_score': maximum_possible_score,
                'time_elapsed_seconds': int(elapsed_time_seconds),
                'experience_earned': int(self.experience_gained),
                'level_increased': level_increased
            }

            print(f"Данные викторины: {quiz_summary}")

            self.account_handler.save_quiz_result(
                quiz_summary
            )

            unlocked_achievements = (
                self.account_handler.check_achievement_progress(
                    quiz_summary
                )
            )

            achievement_names = [
                achievement['name']
                for achievement in unlocked_achievements
            ]
            quiz_summary['unlocked_achievements'] = achievement_names

            print(f"Получено достижений: {len(unlocked_achievements)}")

            print("Викторина успешно завершена")
            return quiz_summary, unlocked_achievements, level_increased

        except Exception as error:
            print(f"Ошибка при финализации викторины: {error}")
            import traceback
            traceback.print_exc()
            return None, [], False

    def calculate_progress(self):
        if self.question_count > 0:
            return (
                self.current_question_index / self.question_count
            ) * 100
        return 0

    def get_time_elapsed(self):
        return self.attempt_start_time.secsTo(
            QDateTime.currentDateTime()
        )