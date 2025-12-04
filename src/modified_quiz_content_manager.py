import random
from quiz_question import QuestionItem
from database_manager import DatabaseManager


class QuestionsManager:
    def __init__(self, elements_storage):
        self.elements_storage = elements_storage
        self.db_manager = DatabaseManager()
        self.questions_collection = self._initialize_questions()
    
    def _initialize_questions(self):
        questions_pool = []
        
        question_count = self.db_manager.get_question_count()
        
        if question_count == 0:
            print("ВНИМАНИЕ: В базе данных нет вопросов!")
            print("Попытка загрузки вопросов из файлов...")
            
            if hasattr(self.elements_storage, '_load_all_data'):
                self.elements_storage._load_all_data()
                question_count = self.db_manager.get_question_count()
                print(f"После загрузки: {question_count} вопросов")
        
        if question_count > 0:
            questions_data = self.db_manager.get_all_questions()
            
            for question_info in questions_data:
                try:
                    question_instance = QuestionItem({
                        'id': question_info['question_id'],
                        'question': question_info['question_text'],
                        'options': question_info.get('options', []),
                        'correct_answer': question_info['correct_answer'],
                        'explanation': question_info.get('explanation', ''),
                        'difficulty': question_info.get('difficulty', 'Средняя'),
                        'category': question_info.get('categories', []),
                        'points': question_info.get('points', 7)
                    })
                    questions_pool.append(question_instance)
                except Exception as e:
                    print(f"Ошибка при создании вопроса: {e}")
            
            print(f"Загружено {len(questions_pool)} вопросов для викторины")
        else:
            print("ВНИМАНИЕ: Не удалось загрузить вопросы. Создаем тестовые...")
            questions_pool = self._create_test_questions()
        
        return questions_pool
    
    def _create_test_questions(self):
        test_questions = []
        
        test_data = [
            {
                'id': 1,
                'question': 'Какой элемент обозначается символом H?',
                'options': ['Гелий', 'Водород', 'Гафний', 'Гольмий'],
                'correct_answer': 'Водород',
                'explanation': 'H - символ водорода.',
                'difficulty': 'Легкая',
                'category': ['Символы', "Элементы"],
                'points': 5
            },
            {
                'id': 2,
                'question': 'Какой элемент обозначается символом O?',
                'options': ['Осмий', 'Олово', 'Кислород', 'Золото'],
                'correct_answer': 'Кислород',
                'explanation': 'O - символ кислорода.',
                'difficulty': 'Легкая',
                'category': ['Символы', "Элементы"],
                'points': 5
            },
            {
                'id': 3,
                'question': 'Какой элемент имеет атомный номер 6?',
                'options': ['Бор', 'Азот', 'Углерод', 'Кислород'],
                'correct_answer': 'Углерод',
                'explanation': 'Углерод имеет атомный номер 6.',
                'difficulty': 'Легкая',
                'category': ['Атомные номера', "Свойства"],
                'points': 5
            },
            {
                'id': 4,
                'question': 'Кто создал периодическую таблицу?',
                'options': ['Эйнштейн', 'Менделеев', 'Кюри', 'Лавуазье'],
                'correct_answer': 'Менделеев',
                'explanation': 'Дмитрий Менделеев создал периодическую таблицу.',
                'difficulty': 'Легкая',
                'category': ['История'],
                'points': 5
            },
            {
                'id': 5,
                'question': 'Какой элемент используется в термометрах?',
                'options': ['Свинец', 'Ртуть', 'Серебро', 'Алюминий'],
                'correct_answer': 'Ртуть',
                'explanation': 'Ртуть используется в термометрах.',
                'difficulty': 'Средняя',
                'category': ['Применение'],
                'points': 7
            },
            {
                'id': 6,
                'question': 'Какой элемент самый легкий?',
                'options': ['Гелий', 'Водород', 'Литий', 'Бериллий'],
                'correct_answer': 'Водород',
                'explanation': 'Водород - самый легкий элемент.',
                'difficulty': 'Легкая',
                'category': ['Свойства'],
                'points': 5
            },
            {
                'id': 7,
                'question': 'Какой металл жидкий при комнатной температуре?',
                'options': ['Ртуть', 'Галлий', 'Цезий', 'Франций'],
                'correct_answer': 'Ртуть',
                'explanation': 'Ртуть - единственный металл, жидкий при комнатной температуре.',
                'difficulty': 'Средняя',
                'category': ['Свойства'],
                'points': 7
            },
            {
                'id': 8,
                'question': 'Какой элемент используется в производстве стали?',
                'options': ['Углерод', 'Кремний', 'Марганец', 'Все вышеперечисленные'],
                'correct_answer': 'Все вышеперечисленные',
                'explanation': 'Все эти элементы используются в производстве стали.',
                'difficulty': 'Средняя',
                'category': ['Применение'],
                'points': 7
            },
            {
                'id': 9,
                'question': 'Какой элемент был открыт на Солнце раньше, чем на Земле?',
                'options': ['Гелий', 'Неон', 'Аргон', 'Ксенон'],
                'correct_answer': 'Гелий',
                'explanation': 'Гелий был обнаружен в спектре Солнца в 1868 году.',
                'difficulty': 'Сложная',
                'category': ['История'],
                'points': 10
            },
            {
                'id': 10,
                'question': 'Какой элемент имеет наибольшую электроотрицательность?',
                'options': ['Фтор', 'Кислород', 'Хлор', 'Азот'],
                'correct_answer': 'Фтор',
                'explanation': 'Фтор имеет электроотрицательность 3.98 по шкале Полинга.',
                'difficulty': 'Средняя',
                'category': ['Свойства'],
                'points': 7
            }
        ]
        
        for q_data in test_data:
            try:
                question_instance = QuestionItem(q_data)
                test_questions.append(question_instance)
            except Exception as e:
                print(f"Ошибка при создании тестового вопроса: {e}")
        
        print(f"Создано {len(test_questions)} тестовых вопросов")
        return test_questions
    
    def get_filtered_questions(self, category_selection="all", difficulty_selection="all", questions_quantity=10):
        print(f"\n=== ФИЛЬТРАЦИЯ ВОПРОСОВ ===")
        print(f"Категория: {category_selection}")
        print(f"Сложность: {difficulty_selection}")
        print(f"Требуемое количество: {questions_quantity}")
        
        if not self.questions_collection:
            print("ВНИМАНИЕ: Коллекция вопросов пуста!")
            self.questions_collection = self._initialize_questions()
        
        total_questions = len(self.questions_collection)
        print(f"Всего вопросов в коллекции: {total_questions}")
        
        if total_questions == 0:
            print("Коллекция пуста, возвращаем тестовые вопросы")
            return self._create_test_questions()[:questions_quantity]
        
        filtered_questions = self.questions_collection.copy()
        
        if category_selection != "all":
            filtered_by_category = []
            
            category_mapping = {
                "elements": ["Символы", "Элементы", "Атомные номера", "Символ", "Элемент"],
                "properties": ["Свойства", "Физические характеристики", "Химические свойства", 
                             "Физические", "Химические"],
                "history": ["История", "Открытие", "Исторические"],
                "application": ["Применение", "Использование", "Практическое применение"]
            }
            
            if category_selection in category_mapping:
                target_categories = category_mapping[category_selection]
                print(f"Ищем категории: {target_categories}")
                
                for q in filtered_questions:
                    question_categories = [cat.lower() for cat in q.categories]
                    
                    question_text = q.question_text.lower()
                    
                    category_match = any(
                        any(target_cat.lower() in question_cat for target_cat in target_categories)
                        for question_cat in question_categories
                    )
                    
                    keyword_match = False
                    if category_selection == "elements":
                        keyword_match = any(word in question_text for word in 
                                          ['символ', 'элемент', 'атомный номер', 'обозначается'])
                    elif category_selection == "properties":
                        keyword_match = any(word in question_text for word in 
                                          ['свойств', 'характеристик', 'температур', 'плотност', 'электроотрицательность'])
                    elif category_selection == "history":
                        keyword_match = any(word in question_text for word in 
                                          ['открыт', 'создал', 'обнаружил', 'назван', 'истори'])
                    elif category_selection == "application":
                        keyword_match = any(word in question_text for word in 
                                          ['используется', 'применяется', 'применение', 'производств', 'изготовлен'])
                    
                    if category_match or keyword_match:
                        filtered_by_category.append(q)
                
                filtered_questions = filtered_by_category
                print(f"После фильтрации по категории осталось: {len(filtered_questions)} вопросов")
            else:
                filtered_questions = [
                    q for q in filtered_questions
                    if any(category_selection.lower() in cat.lower() for cat in q.categories)
                ]
        
        if difficulty_selection != "all":
            difficulty_conversion = {
                "easy": ["Легкая", "легкая", "легкий", "easy"],
                "medium": ["Средняя", "средняя", "средний", "medium"],
                "hard": ["Сложная", "сложная", "сложный", "hard"]
            }
            
            target_difficulties = difficulty_conversion.get(difficulty_selection, [difficulty_selection])
            
            filtered_questions = [
                q for q in filtered_questions
                if any(target.lower() == q.complexity_level.lower() for target in target_difficulties)
            ]
            print(f"После фильтрации по сложности осталось: {len(filtered_questions)} вопросов")
        
        unique_questions = []
        processed_ids = set()
        for question_item in filtered_questions:
            if question_item.identifier not in processed_ids:
                unique_questions.append(question_item)
                processed_ids.add(question_item.identifier)
        
        random.shuffle(unique_questions)
        
        if len(unique_questions) < questions_quantity:
            print(f"Вопросов после фильтрации недостаточно: {len(unique_questions)}")
            print("Добавляем случайные вопросы из всей коллекции...")
            
            all_questions = [q for q in self.questions_collection if q.identifier not in processed_ids]
            random.shuffle(all_questions)
            
            additional_needed = questions_quantity - len(unique_questions)
            additional_to_add = min(additional_needed, len(all_questions))
            
            if additional_to_add > 0:
                unique_questions.extend(all_questions[:additional_to_add])
                print(f"Добавлено {additional_to_add} случайных вопросов")
        
        if len(unique_questions) > questions_quantity:
            final_selection = unique_questions[:questions_quantity]
        else:
            final_selection = unique_questions
        
        print(f"Возвращаем {len(final_selection)} вопросов")
        
        if len(final_selection) == 0:
            print("ВНИМАНИЕ: Не найдено вопросов по заданным критериям!")
            print("Возвращаем случайные вопросы из всей коллекции...")
            all_questions = self.questions_collection.copy()
            random.shuffle(all_questions)
            final_selection = all_questions[:min(questions_quantity, len(all_questions))]
        
        return final_selection
    
    def get_all_categories(self):
        categories = set()
        
        for question in self.questions_collection:
            for category in question.categories:
                categories.add(category)
        
        if len(categories) < 4:
            main_categories = ["Элементы", "Свойства", "История", "Применение",
                             "Символы", "Атомные номера", "Физические характеристики", 
                             "Химические свойства", "Открытие", "Практическое применение"]
            for cat in main_categories:
                categories.add(cat)
        
        return sorted(list(categories))
    
    def get_all_difficulties(self):
        difficulties = set()
        for question in self.questions_collection:
            difficulties.add(question.complexity_level)
        
        if len(difficulties) < 3:
            difficulties.update(["Легкая", "Средняя", "Сложная"])
        
        return sorted(list(difficulties))