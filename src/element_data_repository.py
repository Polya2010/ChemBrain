import json
import os
from chemical_element_data import ChemicalElementData  # Добавлен импорт

class ElementDataRepository:
    def __init__(self):
        self.elements_collection = self._load_elements_from_json()
        self.html_template = self._load_html_template()
        self.color_categories = self._load_color_categories()
        self.element_positions = self._load_element_positions()
        self.quiz_questions = self._load_quiz_questions()
        print(f"Загружено {len(self.quiz_questions)} вопросов из файла")
    
    def _get_data_path(self, filename):
        """Получаем абсолютный путь к файлу в папке data"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(parent_dir, 'data')
        return os.path.join(data_dir, filename)
    
    def _load_html_template(self):
        """Загружает HTML шаблон из файла"""
        try:
            template_path = self._get_data_path('element_template.html')
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f"Файл HTML шаблона не найден: {template_path}")
                return "<div>Ошибка: шаблон не загружен</div>"
        except Exception as e:
            print(f"Ошибка загрузки HTML шаблона: {e}")
            return "<div>Ошибка загрузки шаблона</div>"
    
    def _load_color_categories(self):
        """Загружает цветовые категории из файла"""
        try:
            color_path = self._get_data_path('color_categories.json')
            if os.path.exists(color_path):
                with open(color_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('color_categories', {})
            else:
                print(f"Файл цветовых категорий не найден: {color_path}")
                return {}
        except Exception as e:
            print(f"Ошибка загрузки цветовых категорий: {e}")
            return {}
    
    def _load_element_positions(self):
        """Загружает позиции элементов из файла"""
        try:
            positions_path = self._get_data_path('element_positions.json')
            if os.path.exists(positions_path):
                with open(positions_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    positions = {}
                    for key_str, value in data.get('positions', {}).items():
                        try:
                            positions[int(key_str)] = tuple(value)
                        except (ValueError, TypeError):
                            positions[key_str] = tuple(value)
                    return positions
            else:
                print(f"Файл позиций элементов не найден: {positions_path}")
                return {}
        except Exception as e:
            print(f"Ошибка загрузки позиций элементов: {e}")
            return {}
    
    def _load_quiz_questions(self):
        """Загружает вопросы для викторины из файла"""
        try:
            questions_path = self._get_data_path('quiz_questions.json')
            if os.path.exists(questions_path):
                with open(questions_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get('questions', [])
                    
                    # Проверяем и обновляем структуру вопросов
                    valid_questions = []
                    for q in questions:
                        if 'difficulty' not in q:
                            q['difficulty'] = 'Средняя'
                        if 'category' not in q:
                            q['category'] = ['Общие']
                        if 'points' not in q:
                            difficulty_map = {'Легкая': 5, 'Средняя': 7, 'Сложная': 10}
                            q['points'] = difficulty_map.get(q['difficulty'], 7)
                        valid_questions.append(q)
                    
                    return valid_questions
            else:
                print(f"Файл с вопросами викторины не найден: {questions_path}")
                return self._create_default_questions()
        except Exception as e:
            print(f"Ошибка загрузки вопросов викторины: {e}")
            return self._create_default_questions()
    
    def _create_default_questions(self):
        """Создает минимальный набор вопросов если файл не найден"""
        return [
            {
                "id": 1,
                "question": "Какой символ у элемента 'Водород'?",
                "options": ["H", "O", "He", "N"],
                "correct_answer": "H",
                "explanation": "Символ водорода - H (Hydrogenium).",
                "difficulty": "Легкая",
                "category": ["Символы"],
                "points": 5
            },
            {
                "id": 2,
                "question": "Какой элемент самый распространенный во Вселенной?",
                "options": ["Кислород", "Водород", "Углерод", "Железо"],
                "correct_answer": "Водород",
                "explanation": "Водород составляет около 75% барионной массы Вселенной.",
                "difficulty": "Средняя",
                "category": ["Распространенность"],
                "points": 7
            },
            {
                "id": 3,
                "question": "Какой элемент имеет самую высокую электроотрицательность?",
                "options": ["Фтор", "Кислород", "Хлор", "Азот"],
                "correct_answer": "Фтор",
                "explanation": "Фтор имеет электроотрицательность 3.98 по шкале Полинга.",
                "difficulty": "Сложная",
                "category": ["Свойства"],
                "points": 10
            },
            {
                "id": 4,
                "question": "Какой элемент является жидким при комнатной температуре?",
                "options": ["Ртуть", "Золото", "Алюминий", "Медь"],
                "correct_answer": "Ртуть",
                "explanation": "Ртуть - единственный металл, жидкий при комнатной температуре.",
                "difficulty": "Средняя",
                "category": ["Физические свойства"],
                "points": 7
            },
            {
                "id": 5,
                "question": "Какой газ составляет 78% атмосферы Земли?",
                "options": ["Кислород", "Азот", "Аргон", "Углекислый газ"],
                "correct_answer": "Азот",
                "explanation": "Азот составляет 78% атмосферы Земли.",
                "difficulty": "Легкая",
                "category": ["Состав атмосферы"],
                "points": 5
            }
        ]
    
    def _load_elements_from_json(self):
        try:
            data_dir = os.path.dirname(self._get_data_path(''))
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"Создана папка: {data_dir}")
            
            elements_path = self._get_data_path('elements_data.json')
            if not os.path.exists(elements_path):
                print(f"Файл не найден: {elements_path}")
                return []
                
            with open(elements_path, 'r', encoding='utf-8') as f:
                elements_data = json.load(f)
            
            properties_path = self._get_data_path('element_properties.json')
            if not os.path.exists(properties_path):
                print(f"Файл не найден: {properties_path}")
                return []
                
            with open(properties_path, 'r', encoding='utf-8') as f:
                properties_data = json.load(f)
            
            additional_path = self._get_data_path('element_additional.json')
            if not os.path.exists(additional_path):
                print(f"Файл не найден: {additional_path}")
                return []
                
            with open(additional_path, 'r', encoding='utf-8') as f:
                additional_data = json.load(f)
            
            chemical_elements = []
            
            for element_dict in elements_data["elements"]:
                element = ChemicalElementData(
                    element_dict["symbol"],
                    element_dict["name"],
                    element_dict["atomic_number"],
                    element_dict["atomic_weight"],
                    element_dict["group"],
                    element_dict["period"],
                    element_dict["category"]
                )
                
                atomic_num_str = str(element.atomic_num)
                props = properties_data["properties"].get(atomic_num_str, {})
                additional = additional_data["additional_data"].get(atomic_num_str, {})
                
                element.configure_physical_properties(
                    props.get("electron_config", "Неизвестно"),
                    props.get("electronegativity", "Неизвестно"),
                    props.get("melting_point", "Неизвестно"),
                    props.get("boiling_point", "Неизвестно"),
                    props.get("density", "Неизвестно")
                )
                
                element.set_discovery_info(
                    props.get("discovery_year", "Неизвестно"),
                    props.get("discoverer", "Неизвестно"),
                    props.get("description", "Описание элемента")
                )
                
                element.set_additional_data(
                    additional.get("facts", ["Информация отсутствует"]),
                    additional.get("uses", ["Информация отсутствует"])
                )
                
                chemical_elements.append(element)
            
            print(f"Успешно загружено {len(chemical_elements)} элементов из JSON файлов")
            return chemical_elements
            
        except Exception as e:
            print(f"Ошибка загрузки данных из JSON: {e}")
            return []