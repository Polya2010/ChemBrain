class QuizQuestion:
    def __init__(self, question_data):
        self.question_text = question_data.get("question", "Вопрос не определен")
        self.question_format = "multiple_choice"
        self.answer_choices = question_data.get("options", [])
        self.correct_answer = question_data.get("correct_answer", "")
        self.explanation = question_data.get("explanation", "")
        self.difficulty_level = question_data.get("difficulty", "Средняя")
        self.question_category = question_data.get("category", ["general"])
        self.point_value = question_data.get("points", self._compute_point_value())
        self.id = question_data.get("id", 0)
    
    def _compute_point_value(self):
        point_system = {"Легкая": 5, "Средняя": 7, "Сложная": 10}
        return point_system.get(self.difficulty_level, 7)
    
    def validate_answer(self, user_response):
        return str(user_response).strip() == str(self.correct_answer).strip()