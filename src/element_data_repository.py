import json
import os


class ChemicalElementsStorage:
    def __init__(self):
        self.elements_list = self._load_chemical_elements()
        self.template_html = self._read_html_template()
        self.colors_by_category = self._load_category_colors()
        self.element_coordinates = self._load_coordinates()
        self.quiz_questions_data = self._fetch_questions()
        print(f"Вопросов загружено: {len(self.quiz_questions_data)}")

    def _get_resource_path(self, resource_name):
        current_file = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.dirname(current_file)
        data_folder = os.path.join(parent_folder, 'data')
        return os.path.join(data_folder, resource_name)

    def _read_html_template(self):
        template_file = self._get_resource_path('element_template.html')
        with open(template_file, 'r', encoding='utf-8') as file_content:
            return file_content.read()

    def _load_category_colors(self):
        colors_file = self._get_resource_path('color_categories.json')
        with open(colors_file, 'r', encoding='utf-8') as file_content:
            json_content = json.load(file_content)
            return json_content.get('color_categories', {})

    def _load_coordinates(self):
        coordinates_file = self._get_resource_path('element_positions.json')
        with open(coordinates_file, 'r', encoding='utf-8') as file_content:
            json_content = json.load(file_content)
            coordinates_dict = {}
            positions = json_content.get('positions', {})
            for key_str, value_arr in positions.items():
                try:
                    coordinates_dict[int(key_str)] = tuple(value_arr)
                except (ValueError, TypeError):
                    coordinates_dict[key_str] = tuple(value_arr)
            return coordinates_dict

    def _load_questions_from_file(self, filename, key_name):
        questions_file = self._get_resource_path(filename)
        with open(questions_file, 'r', encoding='utf-8') as file_content:
            json_content = json.load(file_content)
            return json_content.get(key_name, [])

    def _fetch_questions(self):
        all_questions = []

        try:
            main_questions = self._load_questions_from_file(
                'quiz_questions.json',
                'questions'
            )
            print(f"Основных вопросов загружено: {len(main_questions)}")
            all_questions.extend(main_questions)
        except Exception as e:
            print(f"Ошибка загрузки основных вопросов: {e}")

        try:
            basic_questions = self._load_questions_from_file(
                'basic_questions.json',
                'basic_questions'
            )
            print(f"Базовых вопросов загружено: {len(basic_questions)}")
            all_questions.extend(basic_questions)
        except Exception as e:
            print(f"Ошибка загрузки базовых вопросов: {e}")

        try:
            supplementary_questions = self._load_questions_from_file(
                'supplementary_questions.json',
                'supplementary_questions'
            )
            print(f"Дополнительных вопросов загружено: "
                  f"{len(supplementary_questions)}")
            all_questions.extend(supplementary_questions)
        except Exception as e:
            print(f"Ошибка загрузки дополнительных вопросов: {e}")

        try:
            element_questions = self._load_questions_from_file(
                'element_quiz_questions.json',
                'element_questions'
            )
            print(f"Вопросов по элементам загружено: {len(element_questions)}")
            all_questions.extend(element_questions)
        except Exception as e:
            print(f"Ошибка загрузки вопросов по элементам: {e}")

        processed_questions = []
        for question_item in all_questions:
            if 'difficulty' not in question_item:
                question_item['difficulty'] = 'Средняя'
            if 'category' not in question_item:
                question_item['category'] = ['Общие']
            if 'points' not in question_item:
                difficulty_weights = {
                    'Легкая': 5,
                    'Средняя': 7,
                    'Сложная': 10
                }
                question_item['points'] = difficulty_weights.get(
                    question_item['difficulty'],
                    7
                )
            processed_questions.append(question_item)

        print(f"Всего вопросов загружено: {len(processed_questions)}")
        return processed_questions

    def _load_chemical_elements(self):
        from chemical_element_data import ElementInfo

        elements_file = self._get_resource_path('elements_data.json')
        with open(elements_file, 'r', encoding='utf-8') as file_content:
            elements_json = json.load(file_content)

        properties_file = self._get_resource_path('element_properties.json')
        with open(properties_file, 'r', encoding='utf-8') as file_content:
            properties_json = json.load(file_content)

        additional_file = self._get_resource_path('element_additional.json')
        with open(additional_file, 'r', encoding='utf-8') as file_content:
            additional_json = json.load(file_content)

        chemical_elements_collection = []

        for element_item in elements_json["elements"]:
            element_instance = ElementInfo(
                element_item["symbol"],
                element_item["name"],
                element_item["atomic_number"],
                element_item["atomic_weight"],
                element_item["group"],
                element_item["period"],
                element_item["category"]
            )

            atomic_number_str = str(element_instance.atomic_number)
            properties_data = properties_json["properties"].get(
                atomic_number_str,
                {}
            )
            additional_data = additional_json["additional_data"].get(
                atomic_number_str,
                {}
            )

            element_instance.setup_properties(
                properties_data.get("electron_config", "Не указано"),
                properties_data.get("electronegativity", "Не указано"),
                properties_data.get("melting_point", "Не указано"),
                properties_data.get("boiling_point", "Не указано"),
                properties_data.get("density", "Не указано")
            )

            element_instance.setup_history(
                properties_data.get("discovery_year", "Не указано"),
                properties_data.get("discoverer", "Не указано"),
                properties_data.get("description", "Описание элемента")
            )

            element_instance.setup_additional(
                additional_data.get("facts", ["Информация отсутствует"]),
                additional_data.get("uses", ["Информация отсутствует"])
            )

            chemical_elements_collection.append(element_instance)

        print(f"Элементов загружено: {len(chemical_elements_collection)}")
        return chemical_elements_collection
