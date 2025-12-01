import sys
import random
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QPushButton, QLabel, 
    QLineEdit, QComboBox, QTextEdit, QGroupBox, 
    QScrollArea, QStackedWidget, QMessageBox,
    QProgressBar, QRadioButton, QButtonGroup, QTabWidget,
    QDialog, QDialogButtonBox, QFormLayout, QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QPalette, QColor

class ChemicalElementData:
    def __init__(self, symbol, full_name, atomic_num, weight, group_num, period_num, classification):
        self.symbol = symbol
        self.full_name = full_name
        self.atomic_num = atomic_num
        self.weight = weight
        self.group_num = group_num
        self.period_num = period_num
        self.classification = classification
        self.electron_config = ""
        self.electronegativity_val = None
        self.melting_point = None
        self.boiling_point = None
        self.density_val = None
        self.discovery_year = ""
        self.discoverer_info = ""
        self.element_description = ""
        self.interesting_facts_list = []
        self.common_uses_list = []
    
    def configure_physical_properties(self, config, electro, melt, boil, density):
        self.electron_config = config
        self.electronegativity_val = electro
        self.melting_point = melt
        self.boiling_point = boil
        self.density_val = density
    
    def set_discovery_info(self, year, discoverer, description):
        self.discovery_year = year
        self.discoverer_info = discoverer
        self.element_description = description
    
    def set_additional_data(self, facts, uses):
        self.interesting_facts_list = facts
        self.common_uses_list = uses

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
            },
            {
                "id": 6,
                "question": "Какой элемент является самым тугоплавким?",
                "options": ["Вольфрам", "Осмий", "Рений", "Тантал"],
                "correct_answer": "Вольфрам",
                "explanation": "Вольфрам имеет температуру плавления 3422°C.",
                "difficulty": "Сложная",
                "category": ["Физические свойства"],
                "points": 10
            },
            {
                "id": 7,
                "question": "Какой элемент был первым искусственно синтезированным?",
                "options": ["Технеций", "Нептуний", "Плутоний", "Америций"],
                "correct_answer": "Технеций",
                "explanation": "Технеций был синтезирован в 1937 году.",
                "difficulty": "Сложная",
                "category": ["История"],
                "points": 10
            },
            {
                "id": 8,
                "question": "Какой элемент имеет самую высокую плотность?",
                "options": ["Осмий", "Иридий", "Платина", "Золото"],
                "correct_answer": "Осмий",
                "explanation": "Осмий имеет плотность 22.59 г/см³.",
                "difficulty": "Сложная",
                "category": ["Физические свойства"],
                "points": 10
            },
            {
                "id": 9,
                "question": "Какой элемент имеет самую низкую температуру плавления?",
                "options": ["Гелий", "Водород", "Неон", "Кислород"],
                "correct_answer": "Гелий",
                "explanation": "Гелий плавится при -272.2°C.",
                "difficulty": "Сложная",
                "category": ["Физические свойства"],
                "points": 10
            },
            {
                "id": 10,
                "question": "Какой элемент назван в честь России?",
                "options": ["Рутений", "Германий", "Франций", "Полоний"],
                "correct_answer": "Рутений",
                "explanation": "Рутений (Ruthenium) назван в честь России (Ruthenia).",
                "difficulty": "Сложная",
                "category": ["История"],
                "points": 10
            },
            {
                "id": 11,
                "question": "Какой элемент имеет наименьшую атомную массу?",
                "options": ["Водород", "Гелий", "Литий", "Бериллий"],
                "correct_answer": "Водород",
                "explanation": "Водород имеет атомную массу 1.008 а.е.м.",
                "difficulty": "Легкая",
                "category": ["Свойства"],
                "points": 5
            },
            {
                "id": 12,
                "question": "Какой металл используется в термометрах?",
                "options": ["Ртуть", "Серебро", "Золото", "Медь"],
                "correct_answer": "Ртуть",
                "explanation": "Ртуть используется в термометрах из-за её температурных свойств.",
                "difficulty": "Легкая",
                "category": ["Применение"],
                "points": 5
            },
            {
                "id": 13,
                "question": "Какой элемент необходим для фотосинтеза?",
                "options": ["Кислород", "Углерод", "Водород", "Все вышеперечисленные"],
                "correct_answer": "Все вышеперечисленные",
                "explanation": "Все эти элементы необходимы для фотосинтеза.",
                "difficulty": "Средняя",
                "category": ["Биохимия"],
                "points": 7
            },
            {
                "id": 14,
                "question": "Какой элемент самый распространенный в земной коре?",
                "options": ["Кислород", "Кремний", "Алюминий", "Железо"],
                "correct_answer": "Кислород",
                "explanation": "Кислород составляет около 46% массы земной коры.",
                "difficulty": "Средняя",
                "category": ["Геохимия"],
                "points": 7
            },
            {
                "id": 15,
                "question": "Какой элемент образует алмаз?",
                "options": ["Углерод", "Кремний", "Германий", "Бор"],
                "correct_answer": "Углерод",
                "explanation": "Алмаз - это аллотропная модификация углерода.",
                "difficulty": "Легкая",
                "category": ["Свойства"],
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

class ElementInteractiveButton(QPushButton):
    def __init__(self, chemical_element, parent=None):
        super().__init__(parent)
        self.chemical_element = chemical_element
        self._initialize_button_ui()
    
    def _initialize_button_ui(self):
        self.setFixedSize(45, 45)
        self.setText(f"{self.chemical_element.symbol}\n{self.chemical_element.atomic_num}")
        self.setToolTip(f"{self.chemical_element.full_name}")

class PeriodicTableView(QWidget):
    def __init__(self):
        super().__init__()
        self.data_repository = ElementDataRepository()
        self.element_buttons = {}
        self._build_user_interface()
    
    def _build_user_interface(self):
        main_layout = QHBoxLayout()
        
        left_section = self._construct_left_panel()
        right_section = self._construct_right_panel()
        
        main_layout.addLayout(left_section, 3)
        main_layout.addLayout(right_section, 1)
        
        self.setLayout(main_layout)
    
    def _construct_left_panel(self):
        panel_layout = QVBoxLayout()
        
        header_label = QLabel("ПЕРИОДИЧЕСКАЯ СИСТЕМА ЭЛЕМЕНТОВ")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
        panel_layout.addWidget(header_label)
        
        table_widget = self._construct_table_widget()
        panel_layout.addWidget(table_widget)
        
        search_panel = self._construct_search_panel()
        panel_layout.addWidget(search_panel)
        
        return panel_layout
    
    def _construct_right_panel(self):
        panel_layout = QVBoxLayout()
        information_panel = self._construct_information_panel()
        panel_layout.addWidget(information_panel)
        return panel_layout
    
    def _construct_table_widget(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        table_container = QWidget()
        self.table_grid = QGridLayout()
        self.table_grid.setSpacing(1)
        self.table_grid.setContentsMargins(2, 2, 2, 2)
        
        self._arrange_elements_in_grid()
        
        table_container.setLayout(self.table_grid)
        scroll_area.setWidget(table_container)
        return scroll_area
    
    def _arrange_elements_in_grid(self):
        element_positions = self.data_repository.element_positions
        
        for element in self.data_repository.elements_collection:
            if element.atomic_num in element_positions:
                row, column = element_positions[element.atomic_num]
                self._create_element_button(element, row, column)
    
    def _create_element_button(self, element, row, column):
        interactive_button = ElementInteractiveButton(element)
        element_color = self._determine_category_color(element.classification)
        
        button_style = f"""
            QPushButton {{
                background-color: {element_color};
                border: 1px solid #333;
                border-radius: 3px;
                font-weight: bold;
                font-size: 7pt;
                padding: 1px;
            }}
            QPushButton:hover {{
                background-color: {self._modify_color_brightness(element_color, 30)};
                border: 2px solid #000;
            }}
        """
        interactive_button.setStyleSheet(button_style)
        
        interactive_button.clicked.connect(lambda: self._display_element_details(element))
        
        self.table_grid.addWidget(interactive_button, row, column)
        self.element_buttons[element.atomic_num] = interactive_button
    
    def _determine_category_color(self, category):
        color_mapping = self.data_repository.color_categories
        return color_mapping.get(category, "#FFFFFF")
    
    def _modify_color_brightness(self, color_hex, brightness_change):
        if color_hex.startswith("#"):
            red = int(color_hex[1:3], 16)
            green = int(color_hex[3:5], 16)
            blue = int(color_hex[5:7], 16)
            
            red = min(255, red + brightness_change)
            green = min(255, green + brightness_change)
            blue = min(255, blue + brightness_change)
            
            return f"#{red:02x}{green:02x}{blue:02x}"
        return color_hex
    
    def _construct_search_panel(self):
        search_group = QGroupBox("Поиск элемента")
        search_layout = QHBoxLayout()
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Название, символ или номер...")
        self.search_field.textChanged.connect(self._apply_search_highlighting)
        search_layout.addWidget(self.search_field)
        
        self.category_selector = QComboBox()
        categories_list = ["Все категории"] + sorted(list(set(
            [element.classification for element in self.data_repository.elements_collection]
        )))
        self.category_selector.addItems(categories_list)
        self.category_selector.currentTextChanged.connect(self._apply_category_filter)
        search_layout.addWidget(self.category_selector)
        
        search_group.setLayout(search_layout)
        return search_group
    
    def _construct_information_panel(self):
        scrollable_area = QScrollArea()
        scrollable_area.setWidgetResizable(True)
        
        info_container = QWidget()
        info_layout = QVBoxLayout()
        
        self.info_header = QLabel("Выберите элемент")
        self.info_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_header.setStyleSheet("font-size: 14pt; color: #666; margin: 20px;")
        info_layout.addWidget(self.info_header)
        
        self.detailed_info_display = QTextEdit()
        self.detailed_info_display.setReadOnly(True)
        info_layout.addWidget(self.detailed_info_display)
        
        info_container.setLayout(info_layout)
        scrollable_area.setWidget(info_container)
        return scrollable_area
    
    def _display_element_details(self, element):
        information_html = self._generate_detailed_information_html(element)
        self.detailed_info_display.setHtml(information_html)
        self.info_header.setText(f"{element.full_name} ({element.symbol})")
    
    def _generate_detailed_information_html(self, element):
        melting_temp = f"{element.melting_point}°C" if element.melting_point and element.melting_point != "Неизвестно" else "Неизвестно"
        boiling_temp = f"{element.boiling_point}°C" if element.boiling_point and element.boiling_point != "Неизвестно" else "Неизвестно"
        density_val = f"{element.density_val} г/см³" if element.density_val and element.density_val != "Неизвестно" else "Неизвестно"
        electronegativity = f"{element.electronegativity_val}" if element.electronegativity_val and element.electronegativity_val != "Неизвестно" else "Неизвестно"
        
        facts_list = "".join([f"<li style='margin-bottom: 3px;'>{fact}</li>" for fact in element.interesting_facts_list])
        uses_list = "".join([f"<li style='margin-bottom: 3px;'>{use}</li>" for use in element.common_uses_list])
        
        replacements = {
            "CATEGORY_COLOR": self._determine_category_color(element.classification),
            "SYMBOL": element.symbol,
            "NAME": element.full_name,
            "ATOMIC_NUMBER": str(element.atomic_num),
            "ATOMIC_WEIGHT": str(element.weight),
            "GROUP": str(element.group_num),
            "PERIOD": str(element.period_num),
            "CATEGORY": element.classification,
            "ELECTRON_CONFIG": element.electron_config,
            "ELECTRONEGATIVITY": electronegativity,
            "MELTING_POINT": melting_temp,
            "BOILING_POINT": boiling_temp,
            "DENSITY": density_val,
            "DISCOVERY_YEAR": element.discovery_year,
            "DISCOVERER": element.discoverer_info,
            "FACTS_LIST": facts_list,
            "USES_LIST": uses_list,
            "DESCRIPTION": element.element_description
        }
        
        html_content = self.data_repository.html_template
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, str(value))
        
        return html_content
    
    def _apply_search_highlighting(self):
        search_text = self.search_field.text().lower()
        
        for element in self.data_repository.elements_collection:
            button = self.element_buttons.get(element.atomic_num)
            if button:
                is_match = (search_text in element.full_name.lower() or 
                           search_text in element.symbol.lower() or
                           search_text in str(element.atomic_num))
                
                element_color = self._determine_category_color(element.classification)
                if search_text and is_match:
                    border_style = "2px solid #FF0000"
                else:
                    border_style = "1px solid #333"
                
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {element_color};
                        border: {border_style};
                        border-radius: 3px;
                        font-weight: bold;
                        font-size: 7pt;
                        padding: 1px;
                    }}
                    QPushButton:hover {{
                        background-color: {self._modify_color_brightness(element_color, 30)};
                        border: 2px solid #000;
                    }}
                """)
    
    def _apply_category_filter(self):
        selected_category = self.category_selector.currentText()
        
        for element in self.data_repository.elements_collection:
            button = self.element_buttons.get(element.atomic_num)
            if button:
                if selected_category == "Все категории" or element.classification == selected_category:
                    button.setVisible(True)
                else:
                    button.setVisible(False)

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

class StudyUser:
    def __init__(self, username, user_identifier=None):
        self.user_identifier = user_identifier or random.randint(1000, 9999)
        self.username = username
        self.current_level = 1
        self.total_experience = 0
        self.account_creation_date = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        self.unlocked_achievements = []
        self.quiz_history_log = []
        self.correct_answer_streak = 0
        self.max_correct_streak = 0
    
    def add_experience_points(self, experience_points):
        self.total_experience += int(experience_points)
        required_experience = self.current_level * 1000
        if self.total_experience >= required_experience:
            self.current_level += 1
            return True
        return False
    
    def unlock_achievement(self, achievement_data):
        if achievement_data not in self.unlocked_achievements:
            self.unlocked_achievements.append({
                'id': achievement_data['id'],
                'name': achievement_data['name'],
                'unlock_date': QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
            })
            return True
        return False
    
    def record_quiz_result(self, quiz_result_data):
        self.quiz_history_log.append(quiz_result_data)
    
    def update_answer_streak(self, was_correct):
        if was_correct:
            self.correct_answer_streak += 1
            self.max_correct_streak = max(self.max_correct_streak, self.correct_answer_streak)
        else:
            self.correct_answer_streak = 0
    
    def convert_to_dictionary(self):
        return {
            'user_identifier': self.user_identifier,
            'username': self.username,
            'current_level': self.current_level,
            'total_experience': self.total_experience,
            'account_creation_date': self.account_creation_date,
            'unlocked_achievements': self.unlocked_achievements,
            'quiz_history_log': self.quiz_history_log,
            'correct_answer_streak': self.correct_answer_streak,
            'max_correct_streak': self.max_correct_streak
        }
    
    @classmethod
    def create_from_dictionary(cls, data_dict):
        user_instance = cls(data_dict['username'], data_dict['user_identifier'])
        user_instance.current_level = data_dict['current_level']
        user_instance.total_experience = data_dict['total_experience']
        user_instance.account_creation_date = data_dict['account_creation_date']
        user_instance.unlocked_achievements = data_dict.get('unlocked_achievements', [])
        user_instance.quiz_history_log = data_dict.get('quiz_history_log', [])
        user_instance.correct_answer_streak = data_dict.get('correct_answer_streak', 0)
        user_instance.max_correct_streak = data_dict.get('max_correct_streak', 0)
        return user_instance

class UserAccountManager:
    def __init__(self):
        self.active_user = None
        self.registered_users = []
        self.available_achievements = self._initialize_achievements()
        self.load_user_data()
    
    def _get_data_path(self, filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(parent_dir, 'data')
        return os.path.join(data_dir, filename)
    
    def _initialize_achievements(self):
        return [
            {'id': 1, 'name': 'Первые шаги', 'description': 'Пройти первую викторину'},
            {'id': 2, 'name': 'Серия удач', 'description': 'Ответить правильно на 10 вопросов подряд'},
            {'id': 4, 'name': 'Эрудит', 'description': 'Набрать 100% правильных ответов в викторине'},
            {'id': 7, 'name': 'Скорострел', 'description': 'Пройти викторину менее чем за 2 минуты'},
            {'id': 10, 'name': 'Менделеев нашего времени', 'description': 'Достичь 10 уровня'}
        ]
    
    def save_user_data(self):
        data_structure = {
            'users': [user.convert_to_dictionary() for user in self.registered_users],
            'achievements': self.available_achievements
        }
        try:
            data_dir = os.path.dirname(self._get_data_path(''))
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            user_data_path = self._get_data_path('user_progress_data.json')
            with open(user_data_path, 'w', encoding='utf-8') as file:
                json.dump(data_structure, file, ensure_ascii=False, indent=2)
        except Exception as error:
            print(f"Ошибка сохранения данных: {error}")
    
    def load_user_data(self):
        try:
            user_data_path = self._get_data_path('user_progress_data.json')
            if os.path.exists(user_data_path):
                with open(user_data_path, 'r', encoding='utf-8') as file:
                    loaded_data = json.load(file)
                    self.registered_users = [StudyUser.create_from_dictionary(user_data) for user_data in loaded_data.get('users', [])]
                    self.available_achievements = loaded_data.get('achievements', self.available_achievements)
        except Exception as error:
            print(f"Ошибка загрузки данных: {error}")
    
    def register_new_user(self, username):
        if any(user.username == username for user in self.registered_users):
            return False, "Пользователь с таким именем уже существует"
        
        new_user = StudyUser(username)
        self.registered_users.append(new_user)
        self.active_user = new_user
        self.save_user_data()
        return True, f"Пользователь {username} успешно зарегистрирован"
    
    def authenticate_user(self, username):
        for user in self.registered_users:
            if user.username == username:
                self.active_user = user
                return True, f"Добро пожаловать, {username}!"
        return False, "Пользователь не найден"
    
    def user_logout(self):
        self.active_user = None
    
    def evaluate_achievement_progress(self, quiz_data):
        if not self.active_user:
            return []
        
        newly_unlocked = []
        
        if len(self.active_user.quiz_history_log) == 1:
            achievement = self.get_achievement_by_id(1)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if self.active_user.correct_answer_streak >= 10:
            achievement = self.get_achievement_by_id(2)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if quiz_data['correct_answers'] == quiz_data['total_questions']:
            achievement = self.get_achievement_by_id(4)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if quiz_data['time_spent_seconds'] < 120:
            achievement = self.get_achievement_by_id(7)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if self.active_user.current_level >= 10:
            achievement = self.get_achievement_by_id(10)
            if self.active_user.unlock_achievement(achievement):
                newly_unlocked.append(achievement)
        
        if newly_unlocked:
            self.save_user_data()
        
        return newly_unlocked
    
    def get_achievement_by_id(self, achievement_id):
        for achievement in self.available_achievements:
            if achievement['id'] == achievement_id:
                return achievement
        return None

class UserAuthenticationDialog(QDialog):
    def __init__(self, user_manager):
        super().__init__()
        self.user_account_manager = user_manager
        self.setWindowTitle("ChemBrain - Вход в систему")
        self.setModal(True)
        self.initialize_dialog_interface()
    
    def initialize_dialog_interface(self):
        dialog_layout = QVBoxLayout()
        
        input_form_layout = QFormLayout()
        
        self.username_input_field = QLineEdit()
        self.username_input_field.setPlaceholderText("Введите имя пользователя")
        input_form_layout.addRow("Имя пользователя:", self.username_input_field)
        
        dialog_layout.addLayout(input_form_layout)
        
        action_buttons_layout = QHBoxLayout()
        
        self.login_action_button = QPushButton("Войти")
        self.login_action_button.clicked.connect(self.authenticate_user)
        action_buttons_layout.addWidget(self.login_action_button)
        
        self.registration_action_button = QPushButton("Зарегистрироваться")
        self.registration_action_button.clicked.connect(self.register_new_user)
        action_buttons_layout.addWidget(self.registration_action_button)
        
        dialog_layout.addLayout(action_buttons_layout)
        
        self.status_display_label = QLabel("")
        self.status_display_label.setStyleSheet("color: red;")
        dialog_layout.addWidget(self.status_display_label)
        
        self.setLayout(dialog_layout)
    
    def authenticate_user(self):
        username_input = self.username_input_field.text().strip()
        if not username_input:
            self.status_display_label.setText("Введите имя пользователя")
            return
        
        authentication_result, message = self.user_account_manager.authenticate_user(username_input)
        if authentication_result:
            self.accept()
        else:
            self.status_display_label.setText(message)
    
    def register_new_user(self):
        username_input = self.username_input_field.text().strip()
        if not username_input:
            self.status_display_label.setText("Введите имя пользователя")
            return
        
        registration_result, message = self.user_account_manager.register_new_user(username_input)
        if registration_result:
            self.accept()
        else:
            self.status_display_label.setText(message)

class UserProfileScreen(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_account_manager = user_manager
        self.setup_interface()
    
    def setup_interface(self):
        layout = QVBoxLayout()
        
        title = QLabel("ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        info_group = QGroupBox("Основная информация")
        info_layout = QGridLayout()
        
        self.username_label = QLabel()
        self.level_label = QLabel()
        self.xp_label = QLabel()
        self.xp_progress = QProgressBar()
        self.streak_label = QLabel()
        self.quizzes_label = QLabel()
        
        info_layout.addWidget(QLabel("Имя пользователя:"), 0, 0)
        info_layout.addWidget(self.username_label, 0, 1)
        info_layout.addWidget(QLabel("Уровень:"), 1, 0)
        info_layout.addWidget(self.level_label, 1, 1)
        info_layout.addWidget(QLabel("Опыт:"), 2, 0)
        info_layout.addWidget(self.xp_label, 2, 1)
        info_layout.addWidget(QLabel("Прогресс уровня:"), 3, 0)
        info_layout.addWidget(self.xp_progress, 3, 1)
        info_layout.addWidget(QLabel("Текущая серия:"), 4, 0)
        info_layout.addWidget(self.streak_label, 4, 1)
        info_layout.addWidget(QLabel("Пройдено викторин:"), 5, 0)
        info_layout.addWidget(self.quizzes_label, 5, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        achievements_group = QGroupBox("Достижения")
        achievements_layout = QVBoxLayout()
        
        self.achievements_list = QListWidget()
        achievements_layout.addWidget(self.achievements_list)
        
        achievements_group.setLayout(achievements_layout)
        layout.addWidget(achievements_group)
        
        buttons_layout = QHBoxLayout()
        
        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.clicked.connect(self.logout_user)
        buttons_layout.addWidget(self.logout_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def update_profile_display(self):
        if not self.user_account_manager.active_user:
            return
        
        user = self.user_account_manager.active_user
        
        self.username_label.setText(user.username)
        self.level_label.setText(f"{user.current_level}")
        self.xp_label.setText(f"{user.total_experience} XP")
        
        current_level_xp = user.total_experience - ((user.current_level - 1) * 1000)
        progress = (current_level_xp / 1000) * 100
        self.xp_progress.setValue(int(progress))
        
        self.streak_label.setText(f"{user.correct_answer_streak} (макс: {user.max_correct_streak})")
        self.quizzes_label.setText(f"{len(user.quiz_history_log)}")
        
        self.achievements_list.clear()
        for achievement in user.unlocked_achievements:
            item = QListWidgetItem(f"✓ {achievement['name']} ({achievement['unlock_date']})")
            self.achievements_list.addItem(item)
    
    def logout_user(self):
        self.user_account_manager.user_logout()
        self.parent().display_authentication_dialog()

class QuizSession:
    def __init__(self, name, questions, user_manager):
        self.name = name
        self.questions = questions
        self.user_manager = user_manager
        self.current_index = 0
        self.score = 0
        self.total = len(questions)
        self.start_time = QDateTime.currentDateTime()
        self.answers = []
        self.done = False
        self.xp_earned = 0
    
    def get_current_question(self):
        if self.current_index < self.total:
            return self.questions[self.current_index]
        return None
    
    def submit_answer(self, answer):
        current = self.get_current_question()
        if current:
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
        return False
    
    def _finalize_quiz_session(self):
        if not self.user_manager.active_user:
            return None, [], False
        
        completion_xp = len(self.questions) * 5
        self.xp_earned += completion_xp
        
        time_elapsed = self.start_time.secsTo(QDateTime.currentDateTime())
        if time_elapsed < 300:
            speed_bonus = 50
            self.xp_earned += speed_bonus
        
        total_possible_points = sum(q.point_value for q in self.questions)
        accuracy = self.score / total_possible_points if total_possible_points > 0 else 0
        if accuracy >= 0.8:
            accuracy_bonus = int(100 * accuracy)
            self.xp_earned += accuracy_bonus
        
        level_up = self.user_manager.active_user.add_experience_points(int(self.xp_earned))
        
        quiz_data = {
            'timestamp': QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate),
            'quiz_name': self.name,
            'total_questions': self.total,
            'correct_answers': sum(1 for a in self.answers if a['is_correct']),
            'score': self.score,
            'max_score': total_possible_points,
            'time_spent_seconds': int(time_elapsed),
            'xp_earned': int(self.xp_earned),
            'level_up': level_up
        }
        
        self.user_manager.active_user.record_quiz_result(quiz_data)
        
        achievements_unlocked = self.user_manager.evaluate_achievement_progress(quiz_data)
        quiz_data['achievements_unlocked'] = [a['name'] for a in achievements_unlocked]
        
        self.user_manager.save_user_data()
        
        return quiz_data, achievements_unlocked, level_up
    
    def get_progress_percentage(self):
        return (self.current_index / self.total) * 100 if self.total > 0 else 0
    
    def get_elapsed_time(self):
        return self.start_time.secsTo(QDateTime.currentDateTime())

class QuizInterface(QWidget):
    def __init__(self, quiz_manager, user_manager):
        super().__init__()
        self.quiz_manager = quiz_manager
        self.user_manager = user_manager
        self.session = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer_display)
        self.time_elapsed = 0
        self._setup_interface()
    
    def _setup_interface(self):
        layout = QVBoxLayout()
        
        title = QLabel("ХИМИЧЕСКАЯ ВИКТОРИНА")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        self.screen_stack = QStackedWidget()
        
        self.selection_screen = self._create_selection_screen()
        self.screen_stack.addWidget(self.selection_screen)
        
        self.quiz_screen = self._create_quiz_screen()
        self.screen_stack.addWidget(self.quiz_screen)
        
        self.results_screen = self._create_results_screen()
        self.screen_stack.addWidget(self.results_screen)
        
        layout.addWidget(self.screen_stack)
        self.setLayout(layout)
        
        self._show_selection_screen()
    
    def _create_selection_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        if self.user_manager.active_user:
            user_info = QGroupBox("Текущий пользователь")
            user_layout = QHBoxLayout()
            
            user_layout.addWidget(QLabel(f"Пользователь: {self.user_manager.active_user.username}"))
            user_layout.addWidget(QLabel(f"Уровень: {self.user_manager.active_user.current_level}"))
            user_layout.addWidget(QLabel(f"XP: {self.user_manager.active_user.total_experience}"))
            
            user_info.setLayout(user_layout)
            layout.addWidget(user_info)
        
        settings = QGroupBox("Настройки викторины")
        settings_layout = QGridLayout()
        
        settings_layout.addWidget(QLabel("Категория:"), 0, 0)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Все", "Элементы", "Свойства"])
        settings_layout.addWidget(self.category_combo, 0, 1)
        
        settings_layout.addWidget(QLabel("Сложность:"), 1, 0)
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Любая", "Легкая", "Средняя", "Сложная"])
        settings_layout.addWidget(self.difficulty_combo, 1, 1)
        
        settings_layout.addWidget(QLabel("Количество вопросов:"), 2, 0)
        self.count_combo = QComboBox()
        self.count_combo.addItems(["5", "10"])
        settings_layout.addWidget(self.count_combo, 2, 1)
        
        settings.setLayout(settings_layout)
        layout.addWidget(settings)
        
        buttons = QHBoxLayout()
        
        self.start_btn = QPushButton("Начать викторину")
        self.start_btn.setStyleSheet("font-size: 12pt; padding: 10px;")
        self.start_btn.clicked.connect(self._start_quiz_session)
        buttons.addWidget(self.start_btn)
        
        layout.addLayout(buttons)
        widget.setLayout(layout)
        return widget
    
    def _create_quiz_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        info = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        info.addWidget(QLabel("Прогресс:"))
        info.addWidget(self.progress_bar)
        
        self.score_label = QLabel("Счет: 0")
        info.addWidget(self.score_label)
        
        self.time_label = QLabel("Время: 00:00")
        info.addWidget(self.time_label)
        
        layout.addLayout(info)
        
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("font-size: 12pt; margin: 15px;")
        layout.addWidget(self.question_label)
        
        self.answers_widget = QWidget()
        self.answers_layout = QVBoxLayout()
        self.answers_widget.setLayout(self.answers_layout)
        layout.addWidget(self.answers_widget)
        
        nav = QHBoxLayout()
        
        self.next_btn = QPushButton("Следующий вопрос")
        self.next_btn.clicked.connect(self._next_question)
        nav.addWidget(self.next_btn)
        
        self.finish_btn = QPushButton("Завершить викторину")
        self.finish_btn.clicked.connect(self._finish_quiz)
        nav.addWidget(self.finish_btn)
        
        layout.addLayout(nav)
        
        widget.setLayout(layout)
        return widget
    
    def _create_results_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.results_title = QLabel("Результаты викторины")
        self.results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_title.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
        layout.addWidget(self.results_title)
        
        self.results_text = QLabel()
        self.results_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_text.setStyleSheet("font-size: 12pt; margin: 10px;")
        layout.addWidget(self.results_text)
        
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        layout.addWidget(self.details)
        
        buttons = QHBoxLayout()
        
        self.new_btn = QPushButton("Новая викторина")
        self.new_btn.clicked.connect(self._show_selection_screen)
        buttons.addWidget(self.new_btn)
        
        layout.addLayout(buttons)
        
        widget.setLayout(layout)
        return widget
    
    def _show_selection_screen(self):
        self.screen_stack.setCurrentWidget(self.selection_screen)
    
    def _start_quiz_session(self):
        if not self.user_manager.active_user:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, войдите в систему для прохождения викторины")
            return
        
        try:
            category_map = {"Элементы": "elements", "Свойства": "properties", "Все": "all", "Любая": "all"}
            difficulty_map = {"Легкая": "easy", "Средняя": "medium", "Сложная": "hard", "Любая": "all", "Все": "all"}
            
            category = category_map.get(self.category_combo.currentText(), "all")
            difficulty = difficulty_map.get(self.difficulty_combo.currentText(), "all")
            count = int(self.count_combo.currentText())
            
            print(f"Запрос вопросов: категория={category}, сложность={difficulty}, количество={count}")
            
            questions = self.quiz_manager.retrieve_quiz_questions(category, difficulty, count)
            
            if not questions:
                QMessageBox.warning(self, "Ошибка", "Не найдено вопросов с выбранными критериями!")
                return
            
            print(f"Получено {len(questions)} вопросов для викторины")
            
            self.session = QuizSession("Химическая викторина", questions, self.user_manager)
            self.time_elapsed = 0
            self.timer.start(1000)
            
            self._display_current_question()
            self.screen_stack.setCurrentWidget(self.quiz_screen)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске викторины: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _display_current_question(self):
        if not self.session:
            return
        
        question = self.session.get_current_question()
        if not question:
            self._finish_quiz()
            return
        
        progress_value = self.session.get_progress_percentage()
        self.progress_bar.setValue(int(progress_value))
        self.score_label.setText(f"Счет: {self.session.score}")
        
        self.question_label.setText(f"Вопрос {self.session.current_index + 1}: {question.question_text}")
        
        self._clear_answer_options()
        
        if question.question_format == "multiple_choice":
            self._display_multiple_choice(question)
    
    def _clear_answer_options(self):
        for i in reversed(range(self.answers_layout.count())):
            widget = self.answers_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
    
    def _display_multiple_choice(self, question):
        self.buttons_group = QButtonGroup(self)
        
        # Перемешиваем варианты ответов
        options = question.answer_choices.copy()
        random.shuffle(options)
        
        for option in options:
            radio = QRadioButton(str(option))
            radio.setStyleSheet("font-size: 11pt; padding: 8px;")
            self.answers_layout.addWidget(radio)
            self.buttons_group.addButton(radio)
        
        submit_btn = QPushButton("Ответить")
        submit_btn.clicked.connect(self._submit_selected_answer)
        self.answers_layout.addWidget(submit_btn)
    
    def _submit_selected_answer(self):
        selected = self.buttons_group.checkedButton()
        if selected:
            answer = selected.text()
            correct = self.session.submit_answer(answer)
            
            if self.session.done:
                self._finish_quiz()
            else:
                self._display_current_question()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите ответ!")
    
    def _next_question(self):
        if self.session:
            # Отмечаем случайный ответ если пользователь не выбрал
            if not self.buttons_group.checkedButton():
                buttons = self.buttons_group.buttons()
                if buttons:
                    random.choice(buttons).setChecked(True)
            
            selected = self.buttons_group.checkedButton()
            if selected:
                self._submit_selected_answer()
    
    def _finish_quiz(self):
        self.timer.stop()
        if self.session and not self.session.done:
            # Завершаем оставшиеся вопросы
            while not self.session.done:
                self.session.submit_answer("")
            
            quiz_data, achievements, level_up = self.session._finalize_quiz_session()
            self.session.quiz_data = quiz_data
            self.session.new_achievements = achievements
            self.session.level_up = level_up
        
        self._display_results()
        self.screen_stack.setCurrentWidget(self.results_screen)
    
    def _display_results(self):
        if not self.session:
            return
        
        session = self.session
        total_points = sum(q.point_value for q in session.questions)
        percentage = (session.score / total_points) * 100 if total_points > 0 else 0
        
        correct_answers = sum(1 for a in session.answers if a['is_correct'])
        
        summary = f"""
        <h3>Викторина завершена!</h3>
        <p>Правильных ответов: {correct_answers} из {session.total}</p>
        <p>Набрано очков: {session.score} из {total_points}</p>
        <p>Результат: {percentage:.1f}%</p>
        <p>Затраченное время: {int(session.get_elapsed_time())} секунд</p>
        <p>Получено опыта: +{int(session.xp_earned)} XP</p>
        """
        
        if hasattr(session, 'level_up') and session.level_up and self.user_manager.active_user:
            summary += f"<p style='color: green; font-weight: bold;'>🎉 Поздравляем! Вы достигли {self.user_manager.active_user.current_level} уровня!</p>"
        
        # Показываем новые достижения
        if hasattr(session, 'new_achievements') and session.new_achievements:
            achievements_text = "<p style='color: blue;'><b>Новые достижения:</b></p><ul>"
            for achievement in session.new_achievements:
                achievements_text += f"<li>{achievement['name']}</li>"
            achievements_text += "</ul>"
            summary += achievements_text
        
        self.results_text.setText(summary)
        
        details = "<h4>Детальные результаты:</h4><ul>"
        for i, answer in enumerate(session.answers, 1):
            status = "✓ Правильно" if answer['is_correct'] else "✗ Неправильно"
            xp_text = f" (+{int(answer['xp_earned'])} XP)" if answer['is_correct'] else ""
            details += f"""
            <li style="margin-bottom: 10px;">
                <b>Вопрос {i}:</b> {answer['question']}<br>
                <span style="color: {'green' if answer['is_correct'] else 'red'}">
                    {status}{xp_text}
                </span><br>
                Ваш ответ: {answer['user_answer']}<br>
                Правильный ответ: {answer['correct']}
            </li>
            """
        details += "</ul>"
        self.details.setHtml(details)
    
    def _update_timer_display(self):
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.time_label.setText(f"Время: {minutes:02d}:{seconds:02d}")

class ChemistryLearningApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemBrain - Изучение химии")
        self.setGeometry(100, 100, 1400, 900)
        
        self.user_account_manager = UserAccountManager()
        self.element_data_repository = ElementDataRepository()
        
        self.central_navigation_widget = QStackedWidget()
        self.setCentralWidget(self.central_navigation_widget)
        
        self.initialize_main_application_interface()
        self.display_authentication_dialog()
    
    def initialize_main_application_interface(self):
        self.main_interface_widget = QWidget()
        primary_layout = QVBoxLayout()
        
        user_info_panel = QHBoxLayout()
        self.user_information_display = QLabel("Не авторизован")
        user_info_panel.addWidget(self.user_information_display)
        
        self.logout_action_button = QPushButton("Выйти")
        self.logout_action_button.clicked.connect(self.user_sign_out)
        user_info_panel.addWidget(self.logout_action_button)
        
        user_info_panel.addStretch()
        primary_layout.addLayout(user_info_panel)
        
        application_tabs = QTabWidget()
        
        self.periodic_table_interface = PeriodicTableView()
        application_tabs.addTab(self.periodic_table_interface, "Периодическая таблица")
        
        self.quiz_content_manager = QuizContentManager(self.element_data_repository)
        self.quiz_interface = QuizInterface(self.quiz_content_manager, self.user_account_manager)
        application_tabs.addTab(self.quiz_interface, "Химические викторины")
        
        self.user_profile_interface = UserProfileScreen(self.user_account_manager)
        application_tabs.addTab(self.user_profile_interface, "Профиль")
        
        application_tabs.currentChanged.connect(self.on_tab_changed)
        
        primary_layout.addWidget(application_tabs)
        self.main_interface_widget.setLayout(primary_layout)
        
        self.central_navigation_widget.addWidget(self.main_interface_widget)
    
    def on_tab_changed(self, index):
        if index == 2:
            self.user_profile_interface.update_profile_display()
    
    def display_authentication_dialog(self):
        auth_dialog = UserAuthenticationDialog(self.user_account_manager)
        if auth_dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_user_interface_data()
            self.central_navigation_widget.setCurrentWidget(self.main_interface_widget)
        else:
            self.central_navigation_widget.setCurrentWidget(self.main_interface_widget)
    
    def refresh_user_interface_data(self):
        if self.user_account_manager.active_user:
            current_user = self.user_account_manager.active_user
            self.user_information_display.setText(f"Пользователь: {current_user.username} | Уровень: {current_user.current_level} | XP: {current_user.total_experience}")
            self.user_profile_interface.update_profile_display()
        else:
            self.user_information_display.setText("Не авторизован")
    
    def user_sign_out(self):
        self.user_account_manager.user_logout()
        self.refresh_user_interface_data()
        self.display_authentication_dialog()

def launch_application():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = ChemistryLearningApp()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    launch_application()