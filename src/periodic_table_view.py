from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QGroupBox, QScrollArea, QFrame,
    QTextEdit, QMessageBox, QSplitter, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random


class PeriodicTableDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_element = None
        self.elements_storage = None
        self.element_buttons = {}
        self.element_data = {}
        self.empty_cells = {}
        self.search_results = []
        self.original_styles = {}
        self._initialize_ui()
    
    def _initialize_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def _create_left_panel(self):
        panel = QWidget()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(5)
        
        title_label = QLabel("ПЕРИОДИЧЕСКАЯ СИСТЕМА ЭЛЕМЕНТОВ")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #000000;
                padding: 10px;
                border-bottom: 2px solid #333333;
            }
        """)
        panel_layout.addWidget(title_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.table_container = QWidget()
        self.table_layout = QGridLayout()
        self.table_layout.setSpacing(2)
        self.table_layout.setContentsMargins(10, 10, 10, 10)
        
        self.table_container.setLayout(self.table_layout)
        scroll_area.setWidget(self.table_container)
        
        panel_layout.addWidget(scroll_area)
        
        control_panel = self._create_control_panel()
        panel_layout.addWidget(control_panel)
        
        panel.setLayout(panel_layout)
        return panel
    
    def _create_right_panel(self):
        panel = QWidget()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(5, 5, 5, 5)
        panel_layout.setSpacing(10)
        
        self.element_title = QLabel("Выберите элемент")
        self.element_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.element_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.element_title.setStyleSheet("""
            QLabel {
                color: #000000;
                padding: 10px;
                border-bottom: 1px solid #cccccc;
            }
        """)
        panel_layout.addWidget(self.element_title)
        
        self.element_symbol = QLabel("-")
        self.element_symbol.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.element_symbol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.element_symbol.setStyleSheet("""
            QLabel {
                color: #000000;
                padding: 10px;
            }
        """)
        panel_layout.addWidget(self.element_symbol)
        
        self.element_info = QTextEdit()
        self.element_info.setReadOnly(True)
        self.element_info.setMaximumHeight(200)
        self.element_info.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 12px;
                padding: 10px;
                color: #000000;
            }
        """)
        self.element_info.setHtml("""
            <b>Атомный номер:</b> -<br>
            <b>Атомная масса:</b> -<br>
            <b>Группа:</b> -<br>
            <b>Период:</b> -<br>
            <b>Категория:</b> -<br>
            <b>Электронная конфигурация:</b> -<br>
            <b>Электроотрицательность:</b> -<br>
            <b>Температура плавления:</b> -<br>
            <b>Температура кипения:</b> -<br>
            <b>Плотность:</b> -
        """)
        panel_layout.addWidget(self.element_info)
        
        facts_group = QGroupBox("Интересные факты")
        facts_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                color: #000000;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        facts_layout = QVBoxLayout()
        self.facts_text = QTextEdit()
        self.facts_text.setReadOnly(True)
        self.facts_text.setMaximumHeight(100)
        self.facts_text.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: white;
                font-size: 11px;
                padding: 5px;
                color: #000000;
            }
        """)
        self.facts_text.setPlainText("Выберите элемент для отображения информации")
        facts_layout.addWidget(self.facts_text)
        facts_group.setLayout(facts_layout)
        panel_layout.addWidget(facts_group)
        
        history_group = QGroupBox("История открытия")
        history_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                color: #000000;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        history_layout = QVBoxLayout()
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(80)
        self.history_text.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: white;
                font-size: 11px;
                padding: 5px;
                color: #000000;
            }
        """)
        self.history_text.setPlainText("Выберите элемент для отображения информации")
        history_layout.addWidget(self.history_text)
        history_group.setLayout(history_layout)
        panel_layout.addWidget(history_group)
        
        panel_layout.addStretch()
        panel.setLayout(panel_layout)
        return panel
    
    def _create_control_panel(self):
        panel = QWidget()
        panel_layout = QHBoxLayout()
        panel_layout.setContentsMargins(5, 5, 5, 5)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Название, символ или номер...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
                background-color: white;
                color: #000000;
            }
        """)
        self.search_input.returnPressed.connect(self._on_search_clicked)
        self.search_input.textChanged.connect(self._on_search_text_changed)
        
        search_button = QPushButton("🔍 Поиск")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
        """)
        search_button.clicked.connect(self._on_search_clicked)
        
        random_button = QPushButton("🎲 Случайный")
        random_button.setStyleSheet("""
            QPushButton {
                background-color: #6aa84f;
                color: white;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
                border: none;
                margin-left: 5px;
            }
            QPushButton:hover {
                background-color: #5a983f;
            }
        """)
        random_button.clicked.connect(self.display_random_element)
        
        panel_layout.addWidget(self.search_input)
        panel_layout.addWidget(search_button)
        panel_layout.addWidget(random_button)
        panel_layout.addStretch()
        
        panel.setLayout(panel_layout)
        return panel
    
    def _populate_table(self):
        if not self.elements_storage:
            return
        
        self._reset_search_highlight()
        
        elements = self.elements_storage.elements_list
        
        for i in reversed(range(self.table_layout.count())):
            item = self.table_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                widget.deleteLater()
        
        self.element_buttons = {}
        self.element_data = {}
        self.empty_cells = {}
        self.original_styles = {}
        
        element_coordinates = self.elements_storage.element_coordinates
        
        for row in range(10):
            for col in range(18):
                empty_cell = QFrame()
                empty_cell.setFrameShape(QFrame.Shape.Box)
                empty_cell.setLineWidth(1)
                empty_cell.setStyleSheet("border: 1px solid #e0e0e0; background-color: #f9f9f9;")
                empty_cell.setFixedSize(45, 45)
                self.table_layout.addWidget(empty_cell, row, col)
                self.empty_cells[(row, col)] = empty_cell
        
        for element in elements:
            atomic_num = element.atomic_number
            if atomic_num in element_coordinates:
                row, col = element_coordinates[atomic_num]
                self._create_element_button(element, row, col)
    
    def _create_element_button(self, element, row, col):
        button = QPushButton()
        button.setFixedSize(45, 45)
        
        category_color = self._get_category_color(element.category)
        
        base_style = self._create_element_button_style(category_color, is_highlighted=False)
        button.setStyleSheet(base_style)
        
        self.original_styles[element.atomic_number] = base_style
        
        button.setText(f"{element.symbol}\n{element.atomic_number}")
        
        tooltip = f"""<b>{element.name} ({element.symbol})</b><br>
        Атомный номер: {element.atomic_number}<br>
        Атомная масса: {element.atomic_weight}<br>
        Группа: {element.group}, Период: {element.period}<br>
        Категория: {element.category}"""
        button.setToolTip(tooltip)
        
        button.clicked.connect(lambda checked, el=element: self._show_element_info(el))
        
        if (row, col) in self.empty_cells:
            empty_cell = self.empty_cells[(row, col)]
            self.table_layout.removeWidget(empty_cell)
            empty_cell.deleteLater()
            del self.empty_cells[(row, col)]
        
        self.table_layout.addWidget(button, row, col)
        
        self.element_buttons[element.atomic_number] = button
        self.element_data[element.atomic_number] = element
    
    def _create_element_button_style(self, category_color, is_highlighted=False):
        border_width = 3 if is_highlighted else 1
        border_color = "#FF0000" if is_highlighted else "#333333"
        
        style = f"""
            QPushButton {{
                background-color: {category_color};
                color: #000000;
                font-weight: bold;
                border: {border_width}px solid {border_color};
                border-radius: 2px;
                font-size: 9px;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(category_color, 30)};
                border: {border_width}px solid #000000;
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(category_color, 20)};
            }}
        """
        return style
    
    def _get_category_color(self, category):
        if not self.elements_storage:
            return "#FFFFFF"
        
        if hasattr(self.elements_storage, 'colors_by_category'):
            colors = self.elements_storage.colors_by_category
            for key, color in colors.items():
                if key.lower() in str(category).lower():
                    return color
        
        default_colors = {
            "Щелочные металлы": "#FFB3BA",
            "Щелочноземельные металлы": "#FFDFBA",
            "Переходные металлы": "#BAE1FF",
            "Постпереходные металлы": "#E0E0E0",
            "Металлоиды": "#BAFFC9",
            "Неметаллы": "#B5EAD7",
            "Галогены": "#FFFFBA",
            "Благородные газы": "#FFC8E6",
            "Лантаноиды": "#D9C6F0",
            "Актиноиды": "#E6C8A6",
        }
        
        for key, color in default_colors.items():
            if key.lower() in str(category).lower():
                return color
        
        return "#FFFFFF"
    
    def _lighten_color(self, hex_color, amount=20):
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(min(255, c + amount) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return hex_color
    
    def _darken_color(self, hex_color, amount=20):
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(max(0, c - amount) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return hex_color
    
    def _show_element_info(self, element):
        self.selected_element = element
        
        self.element_title.setText(f"{element.name} ({element.symbol})")
        
        self.element_symbol.setText(element.symbol)
        
        basic_info = f"""<b>Атомный номер:</b> {element.atomic_number}<br>
<b>Атомная масса:</b> {element.atomic_weight}<br>
<b>Группа:</b> {element.group if hasattr(element, 'group') else '-'}<br>
<b>Период:</b> {element.period if hasattr(element, 'period') else '-'}<br>
<b>Категория:</b> {element.category if hasattr(element, 'category') else '-'}<br>
<b>Электронная конфигурация:</b> {getattr(element, 'electron_config', 'Не указано')}<br>
<b>Электроотрицательность:</b> {getattr(element, 'electronegativity', 'Не указано')}<br>
<b>Температура плавления:</b> {getattr(element, 'melting_point', 'Не указано')}<br>
<b>Температура кипения:</b> {getattr(element, 'boiling_point', 'Не указано')}<br>
<b>Плотность:</b> {getattr(element, 'density', 'Не указано')}"""
        
        self.element_info.setHtml(basic_info)
        
        facts = getattr(element, 'facts', [])
        if facts and isinstance(facts, list):
            facts_text = ""
            for fact in facts[:5]:
                facts_text += f"• {fact}\n"
            self.facts_text.setPlainText(facts_text)
        else:
            self.facts_text.setPlainText("Интересные факты отсутствуют.")
        
        discovery_year = getattr(element, 'discovery_year', 'Не указано')
        discoverer = getattr(element, 'discoverer', 'Не указано')
        history_info = f"""Год открытия: {discovery_year}
Первооткрыватель: {discoverer}"""
        self.history_text.setPlainText(history_info)
        
        self._animate_element_button(element.atomic_number)
    
    def display_random_element(self):
        if not self.elements_storage:
            QMessageBox.warning(self, "Ошибка", "Данные об элементах не загружены")
            return
        
        elements = self.elements_storage.elements_list
        if elements:
            element = random.choice(elements)
            self._show_element_info(element)
        else:
            QMessageBox.warning(self, "Ошибка", "Нет доступных элементов")
    
    def _animate_element_button(self, atomic_number):
        button = self.element_buttons.get(atomic_number)
        if button and atomic_number in self.element_data:
            element = self.element_data[atomic_number]
            category_color = self._get_category_color(element.category)
            
            highlight_style = self._create_element_button_style(category_color, is_highlighted=True)
            button.setStyleSheet(highlight_style)
            
            QTimer.singleShot(1000, lambda: self._restore_button_style(atomic_number))
    
    def _restore_button_style(self, atomic_number):
        if atomic_number in self.element_buttons and atomic_number in self.element_data:
            button = self.element_buttons[atomic_number]
            
            is_search_result = any(el.atomic_number == atomic_number for el in self.search_results)
            
            if is_search_result:
                element = self.element_data[atomic_number]
                category_color = self._get_category_color(element.category)
                style = self._create_element_button_style(category_color, is_highlighted=True)
            else:
                style = self.original_styles.get(atomic_number)
            
            if style:
                button.setStyleSheet(style)
    
    def _on_search_text_changed(self, text):
        if text.strip() == "":
            self._reset_search_highlight()
    
    def _on_search_clicked(self):
        query = self.search_input.text().strip()
        if query:
            self._search_element(query)
        else:
            QMessageBox.warning(self, "Поиск", "Введите текст для поиска")
    
    def _search_element(self, query):
        if not self.elements_storage:
            QMessageBox.warning(self, "Ошибка", "Данные об элементах не загружены")
            return
        
        self._reset_search_highlight()
        
        results = self.elements_storage.search_elements(query)
        
        if results:
            self.search_results = results
            
            for element in results:
                self._highlight_search_result(element.atomic_number)
            
            self._show_element_info(results[0])
            
            if len(results) > 1:
                QMessageBox.information(self, "Поиск", 
                    f"Найдено {len(results)} элементов. Все найденные элементы подсвечены красной рамкой.")
        else:
            QMessageBox.information(self, "Поиск", 
                f"Элемент '{query}' не найден.")
    
    def _highlight_search_result(self, atomic_number):
        if atomic_number in self.element_buttons and atomic_number in self.element_data:
            button = self.element_buttons[atomic_number]
            element = self.element_data[atomic_number]
            category_color = self._get_category_color(element.category)
            
            style = self._create_element_button_style(category_color, is_highlighted=True)
            button.setStyleSheet(style)
    
    def _reset_search_highlight(self):
        for atomic_num in self.element_buttons:
            if atomic_num in self.original_styles:
                button = self.element_buttons[atomic_num]
                button.setStyleSheet(self.original_styles[atomic_num])
        
        self.search_results = []
    
    def set_elements_storage(self, storage):
        self.elements_storage = storage
        QTimer.singleShot(100, self._populate_table)