import random
from quiz_question import QuestionItem


class QuestionsManager:
    def __init__(self, elements_storage):
        self.elements_storage = elements_storage
        self.questions_collection = self._initialize_questions()
        print(f"Создан менеджер вопросов с {len(self.questions_collection)}"
              " вопросами")

    def _initialize_questions(self):
        questions_pool = []
        questions_data = self.elements_storage.quiz_questions_data

        for question_info in questions_data:
            question_instance = QuestionItem(question_info)
            questions_pool.append(question_instance)

        print(f"Загружено {len(questions_pool)} вопросов для викторины")
        return questions_pool

    def get_filtered_questions(
        self,
        category_selection="all",
        difficulty_selection="all",
        questions_quantity=10
    ):
        filtered_questions = self.questions_collection

        if category_selection != "all":
            if category_selection == "elements":
                filtered_questions = [
                    q for q in filtered_questions
                    if "Символы" in q.categories
                    or "элемент" in q.question_text.lower()
                ]
            elif category_selection == "properties":
                filtered_questions = [
                    q for q in filtered_questions
                    if "Свойства" in q.categories
                    or any(
                        term in q.question_text.lower()
                        for term in [
                            'плотность',
                            'температура',
                            'электроотрицательность',
                            'тугоплавкий'
                        ]
                    )
                ]
            elif category_selection == "history":
                filtered_questions = [
                    q for q in filtered_questions
                    if "История" in q.categories
                    or any(
                        term in q.question_text.lower()
                        for term in ['открыт', 'назван', 'обнаружен']
                    )
                ]
            elif category_selection == "application":
                filtered_questions = [
                    q for q in filtered_questions
                    if "Применение" in q.categories
                    or any(
                        term in q.question_text.lower()
                        for term in [
                            'используется',
                            'применяется',
                            'использование'
                        ]
                    )
                ]

        if difficulty_selection != "all":
            difficulty_conversion = {
                "easy": "Легкая",
                "medium": "Средняя",
                "hard": "Сложная"
            }
            target_difficulty = difficulty_conversion.get(
                difficulty_selection,
                difficulty_selection
            )
            filtered_questions = [
                q for q in filtered_questions
                if q.complexity_level == target_difficulty
            ]

        unique_questions = []
        processed_ids = set()
        for question_item in filtered_questions:
            if question_item.identifier not in processed_ids:
                unique_questions.append(question_item)
                processed_ids.add(question_item.identifier)

        random.shuffle(unique_questions)

        if len(unique_questions) > questions_quantity:
            final_selection = unique_questions[:questions_quantity]
        else:
            final_selection = unique_questions

        return final_selection