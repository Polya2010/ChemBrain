import random
from quiz_question import QuizQuestion

class QuizContentManager:
    def __init__(self, element_repository):
        self.element_repository = element_repository
        self.question_bank = self._load_questions_from_repository()
        print(f"Создан QuizContentManager с {len(self.question_bank)} вопросами")
    
    def _load_questions_from_repository(self):
        questions_collection = []
        question_data_list = self.element_repository.quiz_questions
        
        for question_data in question_data_list:
            try:
                question = QuizQuestion(question_data)
                questions_collection.append(question)
            except Exception as e:
                print(f"Ошибка загрузки вопроса {question_data.get('id', 'unknown')}: {e}")
        
        # Добавляем автоматически сгенерированные вопросы если их недостаточно
        if len(questions_collection) < 15:
            questions_collection.extend(self._generate_extra_questions())
        
        print(f"Загружено {len(questions_collection)} вопросов для викторины")
        
        # Логируем количество вопросов по сложности
        difficulties = {}
        for q in questions_collection:
            difficulties[q.difficulty_level] = difficulties.get(q.difficulty_level, 0) + 1
        print(f"Распределение вопросов по сложности: {difficulties}")
        
        return questions_collection
    
    def _generate_extra_questions(self):
        """Генерирует дополнительные вопросы из элементов"""
        extra_questions = []
        
        # Вопросы на символы элементов
        for element in self.element_repository.elements_collection[:20]:  # Берем первые 20 элементов
            wrong_options = []
            other_elements = [e for e in self.element_repository.elements_collection if e.symbol != element.symbol]
            
            if len(other_elements) >= 3:
                wrong_options = random.sample([e.symbol for e in other_elements], 3)
            
            extra_questions.append(QuizQuestion({
                "id": 1000 + element.atomic_num,
                "question": f"Какой символ у элемента '{element.full_name}'?",
                "options": wrong_options + [element.symbol],
                "correct_answer": element.symbol,
                "explanation": f"Символ элемента {element.full_name} - {element.symbol}.",
                "difficulty": "Легкая",
                "category": ["Символы"],
                "points": 5
            }))
        
        return extra_questions
    
    def retrieve_quiz_questions(self, category_filter="all", difficulty_filter="all", question_count=5):
        try:
            filtered_questions = self.question_bank
            
            # Фильтрация по категории
            if category_filter != "all":
                if category_filter == "elements":
                    filtered_questions = [q for q in filtered_questions if "Символы" in q.question_category or "элемент" in q.question_text.lower()]
                elif category_filter == "properties":
                    filtered_questions = [q for q in filtered_questions if "Свойства" in q.question_category or any(word in q.question_text.lower() for word in ['плотность', 'температура', 'электроотрицательность', 'тугоплавкий'])]
            
            # Фильтрация по сложности
            if difficulty_filter != "all":
                difficulty_map = {"easy": "Легкая", "medium": "Средняя", "hard": "Сложная"}
                desired_difficulty = difficulty_map.get(difficulty_filter, difficulty_filter)
                filtered_questions = [q for q in filtered_questions if q.difficulty_level == desired_difficulty]
            
            print(f"После фильтрации найдено {len(filtered_questions)} вопросов")
            
            # Если вопросов недостаточно, дополняем вопросами из других категорий/сложностей
            if len(filtered_questions) < question_count:
                print(f"Предупреждение: для фильтров (категория: {category_filter}, сложность: {difficulty_filter}) найдено только {len(filtered_questions)} вопросов, нужно {question_count}")
                
                # Дополняем вопросами той же сложности (если есть фильтр по сложности)
                if difficulty_filter != "all":
                    extra_from_same_difficulty = [q for q in self.question_bank if q.difficulty_level == desired_difficulty and q not in filtered_questions]
                    filtered_questions.extend(extra_from_same_difficulty)
                    print(f"Добавлено {len(extra_from_same_difficulty)} вопросов той же сложности")
                
                # Если все еще недостаточно, добавляем вопросы любой сложности
                if len(filtered_questions) < question_count:
                    all_other_questions = [q for q in self.question_bank if q not in filtered_questions]
                    random.shuffle(all_other_questions)
                    filtered_questions.extend(all_other_questions[:question_count - len(filtered_questions)])
                    print(f"Добавлено {min(len(all_other_questions), question_count - len(filtered_questions))} вопросов любой сложности")
            
            # Убедимся, что не возвращаем дубликаты
            unique_questions = []
            seen_ids = set()
            for q in filtered_questions:
                if q.id not in seen_ids:
                    unique_questions.append(q)
                    seen_ids.add(q.id)
            
            # Перемешиваем вопросы
            random.shuffle(unique_questions)
            
            if len(unique_questions) > question_count:
                final_questions = unique_questions[:question_count]
            else:
                final_questions = unique_questions
            
            print(f"Возвращаем {len(final_questions)} вопросов для викторины")
            return final_questions
                
        except Exception as e:
            print(f"Ошибка при получении вопросов: {e}")
            import traceback
            traceback.print_exc()
            # Возвращаем случайные вопросы в случае ошибки
            random.shuffle(self.question_bank)
            return self.question_bank[:min(question_count, len(self.question_bank))]