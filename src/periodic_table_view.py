from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QGroupBox,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QTimer
import random
from element_interactive_button import PeriodicTableButton
from element_data_repository import ChemicalElementsStorage


class PeriodicTableDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.elements_storage = ChemicalElementsStorage()
        self.buttons_dictionary = {}
        self.selected_element = None
        self._initialize_ui()

    def _initialize_ui(self):
        main_container = QHBoxLayout()

        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        main_container.addLayout(left_panel, 3)
        main_container.addLayout(right_panel, 1)

        self.setLayout(main_container)

    def _create_left_panel(self):
        panel_layout = QVBoxLayout()

        header_text = QLabel("ТАБЛИЦА МЕНДЕЛЕЕВА")
        header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_text.setStyleSheet(
            "font-size: 16pt; font-weight: bold; margin: 10px;"
        )
        panel_layout.addWidget(header_text)

        table_area = self._create_table_area()
        panel_layout.addWidget(table_area)

        search_section = self._create_search_section()
        panel_layout.addWidget(search_section)

        return panel_layout

    def _create_right_panel(self):
        panel_layout = QVBoxLayout()
        info_section = self._create_information_section()
        panel_layout.addWidget(info_section)
        return panel_layout

    def _create_table_area(self):
        scrollable_region = QScrollArea()
        scrollable_region.setWidgetResizable(True)

        table_widget = QWidget()
        self.table_layout = QGridLayout()
        self.table_layout.setSpacing(1)
        self.table_layout.setContentsMargins(2, 2, 2, 2)

        self._populate_table_grid()

        table_widget.setLayout(self.table_layout)
        scrollable_region.setWidget(table_widget)
        return scrollable_region

    def _populate_table_grid(self):
        element_locations = self.elements_storage.element_coordinates

        for element_item in self.elements_storage.elements_list:
            if element_item.atomic_number in element_locations:
                row_position, column_position = element_locations[
                    element_item.atomic_number
                ]
                self._add_table_button(
                    element_item,
                    row_position,
                    column_position
                )

    def _add_table_button(
        self,
        element_item,
        row_position,
        column_position
    ):
        element_button = PeriodicTableButton(element_item)
        category_color = self._get_color_by_category(element_item.type_class)

        hover_color = self._adjust_color_brightness(category_color, 30)

        button_style = f"""
            QPushButton {{
                background-color: {category_color};
                border: 1px solid #333;
                border-radius: 3px;
                font-weight: bold;
                font-size: 7pt;
                padding: 1px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 2px solid #000;
            }}
        """
        element_button.setStyleSheet(button_style)

        element_button.clicked.connect(
            lambda checked, el=element_item: self._show_element_information(el)
        )

        self.table_layout.addWidget(
            element_button,
            row_position,
            column_position
        )
        self.buttons_dictionary[element_item.atomic_number] = element_button

    def _get_color_by_category(self, category_name):
        color_mapping = self.elements_storage.colors_by_category
        return color_mapping.get(category_name, "#FFFFFF")

    def _adjust_color_brightness(self, hex_color, adjustment_value):
        if hex_color.startswith("#"):
            red_component = int(hex_color[1:3], 16)
            green_component = int(hex_color[3:5], 16)
            blue_component = int(hex_color[5:7], 16)

            red_component = min(255, red_component + adjustment_value)
            green_component = min(255, green_component + adjustment_value)
            blue_component = min(255, blue_component + adjustment_value)

            return (
                f"#{red_component:02x}{green_component:02x}"
                f"{blue_component:02x}"
            )
        return hex_color

    def _create_search_section(self):
        search_container = QGroupBox("Поиск элементов")
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Введите название, символ или номер..."
        )
        self.search_input.textChanged.connect(self._highlight_search_results)
        search_layout.addWidget(self.search_input)

        self.category_filter = QComboBox()
        categories_set = ["Все категории"] + sorted(
            list(
                set(
                    [
                        element.type_class
                        for element in self.elements_storage.elements_list
                    ]
                )
            )
        )
        self.category_filter.addItems(categories_set)
        self.category_filter.currentTextChanged.connect(
            self._filter_by_category
        )
        search_layout.addWidget(self.category_filter)

        search_container.setLayout(search_layout)
        return search_container

    def _create_information_section(self):
        scrollable_info = QScrollArea()
        scrollable_info.setWidgetResizable(True)

        info_widget = QWidget()
        info_layout = QVBoxLayout()

        self.info_title = QLabel("Выберите элемент")
        self.info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_title.setStyleSheet(
            "font-size: 14pt; color: #666; margin: 20px;"
        )
        info_layout.addWidget(self.info_title)

        self.element_details = QTextEdit()
        self.element_details.setReadOnly(True)
        info_layout.addWidget(self.element_details)

        info_widget.setLayout(info_layout)
        scrollable_info.setWidget(info_widget)
        return scrollable_info

    def _show_element_information(self, element_item):
        self.selected_element = element_item
        element_html = self._generate_element_html(element_item)
        self.element_details.setHtml(element_html)

        title_text = f"{element_item.name} ({element_item.symbol})"
        self.info_title.setText(title_text)

    def _generate_element_html(self, element_item):
        melting_temp_display = (
            f"{element_item.melting_temperature}°C"
            if element_item.melting_temperature
            and element_item.melting_temperature != "Не указано"
            else "Не указано"
        )
        boiling_temp_display = (
            f"{element_item.boiling_temperature}°C"
            if element_item.boiling_temperature
            and element_item.boiling_temperature != "Не указано"
            else "Не указано"
        )
        density_display = (
            f"{element_item.density_value} г/см³"
            if element_item.density_value
            and element_item.density_value != "Не указано"
            else "Не указано"
        )
        electronegativity_display = (
            f"{element_item.electronegativity_value}"
            if element_item.electronegativity_value
            and element_item.electronegativity_value != "Не указано"
            else "Не указано"
        )
        discovery_year_display = element_item.year_of_discovery
        discoverer_display = element_item.discoverer

        facts_html = "".join(
            [
                f"<li style='margin-bottom: 3px;'>{fact_item}</li>"
                for fact_item in element_item.interesting_facts
            ]
        )
        uses_html = "".join(
            [
                f"<li style='margin-bottom: 3px;'>{use_item}</li>"
                for use_item in element_item.common_applications
            ]
        )

        replacement_dict = {
            "CATEGORY_COLOR": self._get_color_by_category(
                element_item.type_class
            ),
            "SYMBOL": element_item.symbol,
            "NAME": element_item.name,
            "ATOMIC_NUMBER": str(element_item.atomic_number),
            "ATOMIC_WEIGHT": str(element_item.atomic_mass),
            "GROUP": str(element_item.group),
            "PERIOD": str(element_item.period),
            "CATEGORY": element_item.type_class,
            "ELECTRON_CONFIG": element_item.electron_configuration,
            "ELECTRONEGATIVITY": electronegativity_display,
            "MELTING_POINT": melting_temp_display,
            "BOILING_POINT": boiling_temp_display,
            "DENSITY": density_display,
            "DISCOVERY_YEAR": discovery_year_display,
            "DISCOVERER": discoverer_display,
            "FACTS_LIST": facts_html,
            "USES_LIST": uses_html,
            "DESCRIPTION": element_item.detailed_description,
        }

        html_content = self.elements_storage.template_html

        for placeholder_key, replacement_value in replacement_dict.items():
            html_content = html_content.replace(
                placeholder_key,
                str(replacement_value)
            )

        return html_content

    def _highlight_search_results(self):
        search_query = self.search_input.text().lower()

        for element_item in self.elements_storage.elements_list:
            button_widget = self.buttons_dictionary.get(
                element_item.atomic_number
            )
            if button_widget:
                matches_search = (
                    search_query in element_item.name.lower()
                    or search_query in element_item.symbol.lower()
                    or search_query in str(element_item.atomic_number)
                )

                element_color = self._get_color_by_category(
                    element_item.type_class
                )
                if search_query and matches_search:
                    border_style = "2px solid #FF0000"
                else:
                    border_style = "1px solid #333"

                adjusted_color = self._adjust_color_brightness(
                    element_color,
                    30
                )
                button_widget.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {element_color};
                        border: {border_style};
                        border-radius: 3px;
                        font-weight: bold;
                        font-size: 7pt;
                        padding: 1px;
                    }}
                    QPushButton:hover {{
                        background-color: {adjusted_color};
                        border: 2px solid #000;
                    }}
                """)

    def _filter_by_category(self):
        selected_filter = self.category_filter.currentText()

        for element_item in self.elements_storage.elements_list:
            button_widget = self.buttons_dictionary.get(
                element_item.atomic_number
            )
            if button_widget:
                is_visible = (
                    selected_filter == "Все категории"
                    or element_item.type_class == selected_filter
                )
                button_widget.setVisible(is_visible)

    def display_random_element(self):
        if self.elements_storage.elements_list:
            random_element = random.choice(
                self.elements_storage.elements_list
            )
            self._show_element_information(random_element)
            self._animate_element_button(random_element.atomic_number)

    def _animate_element_button(self, atomic_number):
        button_widget = self.buttons_dictionary.get(atomic_number)
        if button_widget:
            original_styling = button_widget.styleSheet()

            border_style = (
                "\n                border: 3px solid #FF0000 !important;"
                "\n            "
            )
            button_widget.setStyleSheet(original_styling + border_style)

            QTimer.singleShot(
                1000,
                lambda: button_widget.setStyleSheet(original_styling)
            )
