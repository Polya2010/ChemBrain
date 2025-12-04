import json
import os
from database_manager import DatabaseManager


class ChemicalElementsStorage:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.template_html = self._read_html_template()
        self.colors_by_category = self._load_category_colors()
        self.element_coordinates = self._load_coordinates()
        self._load_all_data()
    
    def _get_resource_path(self, resource_name):
        current_file = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(current_file)
        data_folder = os.path.join(parent_folder, 'data')
        return os.path.join(data_folder, resource_name)
    
    def _read_html_template(self):
        template_file = self._get_resource_path('element_template.html')
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as file_content:
                return file_content.read()
        else:
            return "<h1>{name}</h1><p>Информация об элементе</p>"
    
    def _load_all_data(self):
        elements_file = self._get_resource_path('elements_data.json')
        properties_file = self._get_resource_path('element_properties.json')
        additional_file = self._get_resource_path('element_additional.json')
        
        if all(os.path.exists(f) for f in [elements_file, properties_file, additional_file]):
            self.db_manager.load_elements_from_json(elements_file, properties_file, additional_file)
        
        questions_files = [
            'quiz_questions.json',
            'basic_questions.json',
            'supplementary_questions.json',
            'element_quiz_questions.json',
            'extra_questions.json'
        ]
        
        for q_file in questions_files:
            file_path = self._get_resource_path(q_file)
            if os.path.exists(file_path):
                self.db_manager.load_questions_from_json(file_path)
    
    def _load_category_colors(self):
        colors_file = self._get_resource_path('color_categories.json')
        if os.path.exists(colors_file):
            with open(colors_file, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                return json_content.get('color_categories', {})
        else:
            return {
                "Щелочные металлы": "#FF6666",
                "Щелочноземельные металлы": "#FFDEAD",
                "Переходные металлы": "#FFB6C1",
                "Постпереходные металлы": "#C0C0C0",
                "Металлоиды": "#98FB98",
                "Неметаллы": "#87CEEB",
                "Галогены": "#FFFF99",
                "Благородные газы": "#FFB6C1",
                "Лантаноиды": "#FFB6C1",
                "Актиноиды": "#FFB6C1"
            }
    
    def _load_coordinates(self):
        coordinates_file = self._get_resource_path('element_positions.json')
        if os.path.exists(coordinates_file):
            with open(coordinates_file, 'r', encoding='utf-8') as f:
                json_content = json.load(f)
                coordinates_dict = {}
                positions = json_content.get('positions', {})
                for key_str, value_arr in positions.items():
                    try:
                        coordinates_dict[int(key_str)] = tuple(value_arr)
                    except (ValueError, TypeError):
                        coordinates_dict[key_str] = tuple(value_arr)
                return coordinates_dict
        else:
            return {}
    
    @property
    def elements_list(self):
        from chemical_element_data import ElementInfo
        elements_data = self.db_manager.get_all_elements()
        elements = []
        
        for elem_data in elements_data:
            element = ElementInfo(
                elem_data['symbol'],
                elem_data['name'],
                elem_data['atomic_number'],
                elem_data['atomic_weight'],
                elem_data['element_group'],
                elem_data['period'],
                elem_data['category']
            )
            
            full_data = self.db_manager.get_element_by_number(elem_data['atomic_number'])
            if full_data:
                element.setup_properties(
                    full_data.get('electron_config', 'Не указано'),
                    full_data.get('electronegativity', 'Не указано'),
                    full_data.get('melting_point', 'Не указано'),
                    full_data.get('boiling_point', 'Не указано'),
                    full_data.get('density', 'Не указано')
                )
                
                element.setup_history(
                    full_data.get('discovery_year', 'Не указано'),
                    full_data.get('discoverer', 'Не указано'),
                    full_data.get('description', 'Описание элемента')
                )
                
                element.setup_additional(
                    full_data.get('facts', ['Информация отсутствует']),
                    full_data.get('uses', ['Информация отсутствует'])
                )
            
            elements.append(element)
        
        return elements
    
    def get_element_by_number(self, atomic_number):
        from chemical_element_data import ElementInfo
        elem_data = self.db_manager.get_element_by_number(atomic_number)
        if not elem_data:
            return None
        
        element = ElementInfo(
            elem_data['symbol'],
            elem_data['name'],
            elem_data['atomic_number'],
            elem_data['atomic_weight'],
            elem_data['element_group'],
            elem_data['period'],
            elem_data['category']
        )
        
        element.setup_properties(
            elem_data.get('electron_config', 'Не указано'),
            elem_data.get('electronegativity', 'Не указано'),
            elem_data.get('melting_point', 'Не указано'),
            elem_data.get('boiling_point', 'Не указано'),
            elem_data.get('density', 'Не указано')
        )
        
        element.setup_history(
            elem_data.get('discovery_year', 'Не указано'),
            elem_data.get('discoverer', 'Не указано'),
            elem_data.get('description', 'Описание элемента')
        )
        
        element.setup_additional(
            elem_data.get('facts', ['Информация отсутствует']),
            elem_data.get('uses', ['Информация отсутствует'])
        )
        
        return element
    
    def search_elements(self, query):
        from chemical_element_data import ElementInfo
        results_data = self.db_manager.search_elements(query)
        results = []
        
        for elem_data in results_data:
            element = ElementInfo(
                elem_data['symbol'],
                elem_data['name'],
                elem_data['atomic_number'],
                elem_data['atomic_weight'],
                elem_data['element_group'],
                elem_data['period'],
                elem_data['category']
            )
            
            full_data = self.db_manager.get_element_by_number(elem_data['atomic_number'])
            if full_data:
                element.setup_properties(
                    full_data.get('electron_config', 'Не указано'),
                    full_data.get('electronegativity', 'Не указано'),
                    full_data.get('melting_point', 'Не указано'),
                    full_data.get('boiling_point', 'Не указано'),
                    full_data.get('density', 'Не указано')
                )
                
                element.setup_history(
                    full_data.get('discovery_year', 'Не указано'),
                    full_data.get('discoverer', 'Не указано'),
                    full_data.get('description', 'Описание элемента')
                )
                
                element.setup_additional(
                    full_data.get('facts', ['Информация отсутствует']),
                    full_data.get('uses', ['Информация отсутствует'])
                )
            
            results.append(element)
        
        return results