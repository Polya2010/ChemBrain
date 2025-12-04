class QuestionItem:
    def __init__(self, question_data):
        self.identifier = question_data.get('id', 0)
        self.question_text = question_data.get('question', '')
        self.options = question_data.get('options', [])
        self.correct_answer = question_data.get('correct_answer', '')
        self.explanation = question_data.get('explanation', '')
        self.complexity_level = question_data.get('difficulty', 'Средняя')
        self.categories = question_data.get('category', [])
        self.points = question_data.get('points', 7)
        
        if isinstance(self.categories, str):
            self.categories = [self.categories]
    
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer
    
    def __str__(self):
        return f"Вопрос {self.identifier}: {self.question_text[:50]}..."
    
    def to_dict(self):
        return {
            'id': self.identifier,
            'question': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'difficulty': self.complexity_level,
            'category': self.categories,
            'points': self.points
        }