from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
    QLabel, QLineEdit, QComboBox, QTextEdit, QGroupBox, 
    QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
import random
from element_interactive_button import ElementInteractiveButton
from element_data_repository import ElementDataRepository

class PeriodicTableView(QWidget):
    def __init__(self):
        super().__init__()
        self.data_repository = ElementDataRepository()
        self.element_buttons = {}
        self.current_element = None
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
        
        header_label = QLabel("ПЕРИОДИЧЕСКАЯ СИСТЕМА ЭЛЕМЕНТОВ (Ctrl+M)")
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
        self.current_element = element
        information_html = self._generate_detailed_information_html(element)
        self.detailed_info_display.setHtml(information_html)
        
        self.info_header.setText(f"{element.full_name} ({element.symbol})")
    
    def _generate_detailed_information_html(self, element):
        # Форматируем данные
        melting_temp = f"{element.melting_point}°C" if element.melting_point and element.melting_point != "Неизвестно" else "Неизвестно"
        boiling_temp = f"{element.boiling_point}°C" if element.boiling_point and element.boiling_point != "Неизвестно" else "Неизвестно"
        density_val = f"{element.density_val} г/см³" if element.density_val and element.density_val != "Неизвестно" else "Неизвестно"
        electronegativity = f"{element.electronegativity_val}" if element.electronegativity_val and element.electronegativity_val != "Неизвестно" else "Неизвестно"
        discovery_year = element.discovery_year
        discoverer = element.discoverer_info
        
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
            "DISCOVERY_YEAR": discovery_year,
            "DISCOVERER": discoverer,
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
    
    def show_random_element(self):
        """Показать случайный элемент"""
        if self.data_repository.elements_collection:
            random_element = random.choice(self.data_repository.elements_collection)
            self._display_element_details(random_element)
            self._highlight_element_button(random_element.atomic_num)
    
    def _highlight_element_button(self, atomic_num):
        """Выделить кнопку элемента"""
        button = self.element_buttons.get(atomic_num)
        if button:
            original_style = button.styleSheet()
            
            # Временное выделение
            button.setStyleSheet(original_style + """
                border: 3px solid #FF0000 !important;
            """)
            
            # Возвращаем оригинальный стиль через 1 секунду
            QTimer.singleShot(1000, lambda: button.setStyleSheet(original_style))