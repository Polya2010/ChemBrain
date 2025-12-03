class QuestionItem:
    def __init__(self, question_info):
        self.question_text = question_info.get(
            "question",
            "Текст вопроса отсутствует"
        )
        self.question_type = "multiple_choice"
        self.possible_answers = question_info.get("options", [])
        self.correct_response = question_info.get("correct_answer", "")
        self.explanation_text = question_info.get("explanation", "")
        self.complexity_level = question_info.get("difficulty", "Средняя")
        self.categories = question_info.get("category", ["general"])
        self.score_value = question_info.get(
            "points",
            self._calculate_score()
        )
        self.identifier = question_info.get("id", 0)

    def _calculate_score(self):
        score_mapping = {
            "Легкая": 5,
            "Средняя": 7,
            "Сложная": 10
        }
        return score_mapping.get(self.complexity_level, 7)

    def check_answer(self, user_response):
        user_answer = str(user_response).strip()
        correct_answer = str(self.correct_response).strip()
        return user_answer == correct_answer
