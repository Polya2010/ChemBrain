import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QPushButton, QLabel, 
    QLineEdit, QComboBox, QTextEdit, QGroupBox, 
    QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class ChemicalElement:
    """Класс для хранения данных о химическом элементе"""
    
    def __init__(self, symbol, name, atomic_number, atomic_mass, group, period, category):
        self.symbol = symbol
        self.name = name
        self.atomic_number = atomic_number
        self.atomic_mass = atomic_mass
        self.group = group
        self.period = period
        self.category = category
        self.electron_config = ""
        self.electronegativity = None
        self.melting_temperature = None
        self.boiling_temperature = None
        self.density_value = None
        self.year_discovered = ""
        self.discoverer_name = ""
        self.element_description = ""
        self.interesting_facts = []
        self.common_uses = []
    
    def set_physical_properties(self, electron_config, electronegativity, melting_temp, boiling_temp, density):
        """Установка физических свойств элемента"""
        self.electron_config = electron_config
        self.electronegativity = electronegativity
        self.melting_temperature = melting_temp
        self.boiling_temperature = boiling_temp
        self.density_value = density
    
    def set_discovery_info(self, year, discoverer, description):
        """Установка информации об открытии элемента"""
        self.year_discovered = year
        self.discoverer_name = discoverer
        self.element_description = description
    
    def set_additional_info(self, facts, uses):
        """Установка дополнительной информации"""
        self.interesting_facts = facts
        self.common_uses = uses

class ElementDatabase:
    """База данных химических элементов"""
    
    def __init__(self):
        self.all_elements = self._initialize_elements()
    
    def _initialize_elements(self):
        """Инициализация всех химических элементов"""
        elements_data = [
            # Период 1
            ("H", "Водород", 1, 1.008, 1, 1, "Неметаллы"),
            ("He", "Гелий", 2, 4.0026, 18, 1, "Инертные газы"),
            
            # Период 2
            ("Li", "Литий", 3, 6.94, 1, 2, "Щелочные металлы"),
            ("Be", "Бериллий", 4, 9.0122, 2, 2, "Щелочноземельные металлы"),
            ("B", "Бор", 5, 10.81, 13, 2, "Металлоиды"),
            ("C", "Углерод", 6, 12.011, 14, 2, "Неметаллы"),
            ("N", "Азот", 7, 14.007, 15, 2, "Неметаллы"),
            ("O", "Кислород", 8, 15.999, 16, 2, "Неметаллы"),
            ("F", "Фтор", 9, 18.998, 17, 2, "Галогены"),
            ("Ne", "Неон", 10, 20.180, 18, 2, "Инертные газы"),
            
            # Период 3
            ("Na", "Натрий", 11, 22.990, 1, 3, "Щелочные металлы"),
            ("Mg", "Магний", 12, 24.305, 2, 3, "Щелочноземельные металлы"),
            ("Al", "Алюминий", 13, 26.982, 13, 3, "Постпереходные металлы"),
            ("Si", "Кремний", 14, 28.085, 14, 3, "Металлоиды"),
            ("P", "Фосфор", 15, 30.974, 15, 3, "Неметаллы"),
            ("S", "Сера", 16, 32.06, 16, 3, "Неметаллы"),
            ("Cl", "Хлор", 17, 35.45, 17, 3, "Галогены"),
            ("Ar", "Аргон", 18, 39.948, 18, 3, "Инертные газы"),
            
            # Период 4
            ("K", "Калий", 19, 39.098, 1, 4, "Щелочные металлы"),
            ("Ca", "Кальций", 20, 40.078, 2, 4, "Щелочноземельные металлы"),
            ("Sc", "Скандий", 21, 44.956, 3, 4, "Переходные металлы"),
            ("Ti", "Титан", 22, 47.867, 4, 4, "Переходные металлы"),
            ("V", "Ванадий", 23, 50.942, 5, 4, "Переходные металлы"),
            ("Cr", "Хром", 24, 51.996, 6, 4, "Переходные металлы"),
            ("Mn", "Марганец", 25, 54.938, 7, 4, "Переходные металлы"),
            ("Fe", "Железо", 26, 55.845, 8, 4, "Переходные металлы"),
            ("Co", "Кобальт", 27, 58.933, 9, 4, "Переходные металлы"),
            ("Ni", "Никель", 28, 58.693, 10, 4, "Переходные металлы"),
            ("Cu", "Медь", 29, 63.546, 11, 4, "Переходные металлы"),
            ("Zn", "Цинк", 30, 65.38, 12, 4, "Переходные металлы"),
            ("Ga", "Галлий", 31, 69.723, 13, 4, "Постпереходные металлы"),
            ("Ge", "Германий", 32, 72.630, 14, 4, "Металлоиды"),
            ("As", "Мышьяк", 33, 74.922, 15, 4, "Металлоиды"),
            ("Se", "Селен", 34, 78.971, 16, 4, "Неметаллы"),
            ("Br", "Бром", 35, 79.904, 17, 4, "Галогены"),
            ("Kr", "Криптон", 36, 83.798, 18, 4, "Инертные газы"),
            
            # Период 5
            ("Rb", "Рубидий", 37, 85.468, 1, 5, "Щелочные металлы"),
            ("Sr", "Стронций", 38, 87.62, 2, 5, "Щелочноземельные металлы"),
            ("Y", "Иттрий", 39, 88.906, 3, 5, "Переходные металлы"),
            ("Zr", "Цирконий", 40, 91.224, 4, 5, "Переходные металлы"),
            ("Nb", "Ниобий", 41, 92.906, 5, 5, "Переходные металлы"),
            ("Mo", "Молибден", 42, 95.95, 6, 5, "Переходные металлы"),
            ("Tc", "Технеций", 43, 98, 7, 5, "Переходные металлы"),
            ("Ru", "Рутений", 44, 101.07, 8, 5, "Переходные металлы"),
            ("Rh", "Родий", 45, 102.91, 9, 5, "Переходные металлы"),
            ("Pd", "Палладий", 46, 106.42, 10, 5, "Переходные металлы"),
            ("Ag", "Серебро", 47, 107.87, 11, 5, "Переходные металлы"),
            ("Cd", "Кадмий", 48, 112.41, 12, 5, "Переходные металлы"),
            ("In", "Индий", 49, 114.82, 13, 5, "Постпереходные металлы"),
            ("Sn", "Олово", 50, 118.71, 14, 5, "Постпереходные металлы"),
            ("Sb", "Сурьма", 51, 121.76, 15, 5, "Металлоиды"),
            ("Te", "Теллур", 52, 127.60, 16, 5, "Металлоиды"),
            ("I", "Иод", 53, 126.90, 17, 5, "Галогены"),
            ("Xe", "Ксенон", 54, 131.29, 18, 5, "Инертные газы"),
            
            # Период 6
            ("Cs", "Цезий", 55, 132.91, 1, 6, "Щелочные металлы"),
            ("Ba", "Барий", 56, 137.33, 2, 6, "Щелочноземельные металлы"),
            ("La", "Лантан", 57, 138.91, 3, 6, "Лантаноиды"),
            ("Ce", "Церий", 58, 140.12, 3, 6, "Лантаноиды"),
            ("Pr", "Празеодим", 59, 140.91, 3, 6, "Лантаноиды"),
            ("Nd", "Неодим", 60, 144.24, 3, 6, "Лантаноиды"),
            ("Pm", "Прометий", 61, 145, 3, 6, "Лантаноиды"),
            ("Sm", "Самарий", 62, 150.36, 3, 6, "Лантаноиды"),
            ("Eu", "Европий", 63, 151.96, 3, 6, "Лантаноиды"),
            ("Gd", "Гадолиний", 64, 157.25, 3, 6, "Лантаноиды"),
            ("Tb", "Тербий", 65, 158.93, 3, 6, "Лантаноиды"),
            ("Dy", "Диспрозий", 66, 162.50, 3, 6, "Лантаноиды"),
            ("Ho", "Гольмий", 67, 164.93, 3, 6, "Лантаноиды"),
            ("Er", "Эрбий", 68, 167.26, 3, 6, "Лантаноиды"),
            ("Tm", "Тулий", 69, 168.93, 3, 6, "Лантаноиды"),
            ("Yb", "Иттербий", 70, 173.05, 3, 6, "Лантаноиды"),
            ("Lu", "Лютеций", 71, 174.97, 3, 6, "Лантаноиды"),
            ("Hf", "Гафний", 72, 178.49, 4, 6, "Переходные металлы"),
            ("Ta", "Тантал", 73, 180.95, 5, 6, "Переходные металлы"),
            ("W", "Вольфрам", 74, 183.84, 6, 6, "Переходные металлы"),
            ("Re", "Рений", 75, 186.21, 7, 6, "Переходные металлы"),
            ("Os", "Осмий", 76, 190.23, 8, 6, "Переходные металлы"),
            ("Ir", "Иридий", 77, 192.22, 9, 6, "Переходные металлы"),
            ("Pt", "Платина", 78, 195.08, 10, 6, "Переходные металлы"),
            ("Au", "Золото", 79, 196.97, 11, 6, "Переходные металлы"),
            ("Hg", "Ртуть", 80, 200.59, 12, 6, "Переходные металлы"),
            ("Tl", "Таллий", 81, 204.38, 13, 6, "Постпереходные металлы"),
            ("Pb", "Свинец", 82, 207.2, 14, 6, "Постпереходные металлы"),
            ("Bi", "Висмут", 83, 208.98, 15, 6, "Постпереходные металлы"),
            ("Po", "Полоний", 84, 209, 16, 6, "Металлоиды"),
            ("At", "Астат", 85, 210, 17, 6, "Галогены"),
            ("Rn", "Радон", 86, 222, 18, 6, "Инертные газы"),
            
            # Период 7
            ("Fr", "Франций", 87, 223, 1, 7, "Щелочные металлы"),
            ("Ra", "Радий", 88, 226, 2, 7, "Щелочноземельные металлы"),
            ("Ac", "Актиний", 89, 227, 3, 7, "Актиноиды"),
            ("Th", "Торий", 90, 232.04, 3, 7, "Актиноиды"),
            ("Pa", "Протактиний", 91, 231.04, 3, 7, "Актиноиды"),
            ("U", "Уран", 92, 238.03, 3, 7, "Актиноиды"),
            ("Np", "Нептуний", 93, 237, 3, 7, "Актиноиды"),
            ("Pu", "Плутоний", 94, 244, 3, 7, "Актиноиды"),
            ("Am", "Америций", 95, 243, 3, 7, "Актиноиды"),
            ("Cm", "Кюрий", 96, 247, 3, 7, "Актиноиды"),
            ("Bk", "Берклий", 97, 247, 3, 7, "Актиноиды"),
            ("Cf", "Калифорний", 98, 251, 3, 7, "Актиноиды"),
            ("Es", "Эйнштейний", 99, 252, 3, 7, "Актиноиды"),
            ("Fm", "Фермий", 100, 257, 3, 7, "Актиноиды"),
            ("Md", "Менделевий", 101, 258, 3, 7, "Актиноиды"),
            ("No", "Нобелий", 102, 259, 3, 7, "Актиноиды"),
            ("Lr", "Лоуренсий", 103, 266, 3, 7, "Актиноиды"),
            ("Rf", "Резерфордий", 104, 267, 4, 7, "Переходные металлы"),
            ("Db", "Дубний", 105, 268, 5, 7, "Переходные металлы"),
            ("Sg", "Сиборгий", 106, 269, 6, 7, "Переходные металлы"),
            ("Bh", "Борий", 107, 270, 7, 7, "Переходные металлы"),
            ("Hs", "Хассий", 108, 269, 8, 7, "Переходные металлы"),
            ("Mt", "Мейтнерий", 109, 278, 9, 7, "Переходные металлы"),
            ("Ds", "Дармштадтий", 110, 281, 10, 7, "Переходные металлы"),
            ("Rg", "Рентгений", 111, 282, 11, 7, "Переходные металлы"),
            ("Cn", "Коперниций", 112, 285, 12, 7, "Переходные металлы"),
            ("Nh", "Нихоний", 113, 286, 13, 7, "Постпереходные металлы"),
            ("Fl", "Флеровий", 114, 289, 14, 7, "Постпереходные металлы"),
            ("Mc", "Московий", 115, 290, 15, 7, "Постпереходные металлы"),
            ("Lv", "Ливерморий", 116, 293, 16, 7, "Постпереходные металлы"),
            ("Ts", "Теннессин", 117, 294, 17, 7, "Галогены"),
            ("Og", "Оганесон", 118, 294, 18, 7, "Инертные газы")
        ]
        
        elements_list = []
        for data in elements_data:
            element = ChemicalElement(*data)
            self._add_element_properties(element)
            elements_list.append(element)
        
        return elements_list
    
    def _add_element_properties(self, element):
        """Добавление свойств для элемента"""
        properties_data = self._get_properties_data(element.atomic_number)
        element.set_physical_properties(*properties_data[:5])
        element.set_discovery_info(*properties_data[5:8])
        element.set_additional_info(*properties_data[8:])
    
    def _get_properties_data(self, atomic_number):
        """Получение данных о свойствах элемента"""
        properties = {
            1: ("1s¹", 2.20, -259.16, -252.87, 0.0000899, 1766, "Генри Кавендиш", 
                "Самый легкий и распространенный элемент во Вселенной", 
                ["Составляет 75% массы Вселенной", "Первый элемент после Большого взрыва"],
                ["Производство аммиака", "Ракетное топливо", "Металлургия"]),
            2: ("1s²", None, -272.2, -268.93, 0.0001785, 1868, "Пьер Жансен", 
                "Второй по легкости элемент", 
                ["Используется в воздухоплавании", "Негорючий газ"],
                ["Дирижабли", "Криогеника", "Дыхательные смеси"]),
            # ... аналогично для остальных элементов
        }
        return properties.get(atomic_number, ("Неизвестно", "Неизвестно", "Неизвестно", "Неизвестно", 
                                           "Неизвестно", "Неизвестно", "Неизвестно", "Описание элемента",
                                           ["Интересный факт"], ["Применение элемента"]))

class ElementButton(QPushButton):
    """Кнопка элемента периодической таблицы"""
    
    def __init__(self, element_data, parent=None):
        super().__init__(parent)
        self.element_data = element_data
        self.setup_appearance()
    
    def setup_appearance(self):
        """Настройка внешнего вида кнопки"""
        self.setFixedSize(60, 60)
        self.setText(f"{self.element_data.symbol}\n{self.element_data.atomic_number}")
        self.setToolTip(f"{self.element_data.name} ({self.element_data.symbol})")

class PeriodicTableView(QWidget):
    """Виджет для отображения периодической таблицы"""
    
    def __init__(self):
        super().__init__()
        self.element_database = ElementDatabase()
        self.element_buttons = {}
        self.initialize_interface()
    
    def initialize_interface(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QHBoxLayout()
        
        left_section = self.create_left_section()
        right_section = self.create_right_section()
        
        main_layout.addLayout(left_section, 2)
        main_layout.addLayout(right_section, 1)
        
        self.setLayout(main_layout)
    
    def create_left_section(self):
        """Создание левой части интерфейса"""
        left_layout = QVBoxLayout()
        
        title = QLabel("ПЕРИОДИЧЕСКАЯ СИСТЕМА ХИМИЧЕСКИХ ЭЛЕМЕНТОВ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
        left_layout.addWidget(title)
        
        table_widget = self.create_periodic_table()
        left_layout.addWidget(table_widget)
        
        search_panel = self.create_search_panel()
        left_layout.addWidget(search_panel)
        
        return left_layout
    
    def create_right_section(self):
        """Создание правой части интерфейса"""
        right_layout = QVBoxLayout()
        info_panel = self.create_info_panel()
        right_layout.addWidget(info_panel)
        return right_layout
    
    def create_periodic_table(self):
        """Создание периодической таблицы"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        table_container = QWidget()
        self.table_grid = QGridLayout()
        self.table_grid.setSpacing(2)
        self.table_grid.setContentsMargins(10, 10, 10, 10)
        
        self.place_elements_in_grid()
        
        table_container.setLayout(self.table_grid)
        scroll_area.setWidget(table_container)
        return scroll_area
    
    def place_elements_in_grid(self):
        """Размещение элементов в сетке"""
        element_positions = self.get_element_positions()
        
        for element in self.element_database.all_elements:
            if element.atomic_number in element_positions:
                row, column = element_positions[element.atomic_number]
                self.create_element_button(element, row, column)
    
    def get_element_positions(self):
        """Получение позиций элементов в таблице"""
        return {
            # Период 1
            1: (0, 0),   2: (0, 17),
            
            # Период 2
            3: (1, 0),   4: (1, 1),   5: (1, 12),  6: (1, 13),  7: (1, 14),  
            8: (1, 15),  9: (1, 16),  10: (1, 17),
            
            # Период 3
            11: (2, 0),  12: (2, 1),  13: (2, 12), 14: (2, 13), 15: (2, 14), 
            16: (2, 15), 17: (2, 16), 18: (2, 17),
            
            # Период 4
            19: (3, 0),  20: (3, 1),  21: (3, 2),  22: (3, 3),  23: (3, 4),  
            24: (3, 5),  25: (3, 6),  26: (3, 7),  27: (3, 8),  28: (3, 9),
            29: (3, 10), 30: (3, 11), 31: (3, 12), 32: (3, 13), 33: (3, 14), 
            34: (3, 15), 35: (3, 16), 36: (3, 17),
            
            # Период 5
            37: (4, 0),  38: (4, 1),  39: (4, 2),  40: (4, 3),  41: (4, 4),  
            42: (4, 5),  43: (4, 6),  44: (4, 7),  45: (4, 8),  46: (4, 9),
            47: (4, 10), 48: (4, 11), 49: (4, 12), 50: (4, 13), 51: (4, 14), 
            52: (4, 15), 53: (4, 16), 54: (4, 17),
            
            # Период 6
            55: (5, 0),  56: (5, 1),  
            # Лантаноиды
            57: (8, 3),  58: (8, 4),  59: (8, 5),  60: (8, 6),  61: (8, 7),  
            62: (8, 8),  63: (8, 9),  64: (8, 10), 65: (8, 11), 66: (8, 12),
            67: (8, 13), 68: (8, 14), 69: (8, 15), 70: (8, 16), 71: (8, 17),
            # Продолжение 6 периода
            72: (5, 2),  73: (5, 3),  74: (5, 4),  75: (5, 5),  76: (5, 6),  
            77: (5, 7),  78: (5, 8),  79: (5, 9),  80: (5, 10), 81: (5, 11),
            82: (5, 12), 83: (5, 13), 84: (5, 14), 85: (5, 15), 86: (5, 17),
            
            # Период 7
            87: (6, 0),  88: (6, 1),
            # Актиноиды
            89: (9, 3),  90: (9, 4),  91: (9, 5),  92: (9, 6),  93: (9, 7),  
            94: (9, 8),  95: (9, 9),  96: (9, 10), 97: (9, 11), 98: (9, 12),
            99: (9, 13), 100: (9, 14), 101: (9, 15), 102: (9, 16), 103: (9, 17),
            # Продолжение 7 периода
            104: (6, 2), 105: (6, 3), 106: (6, 4), 107: (6, 5), 108: (6, 6), 
            109: (6, 7), 110: (6, 8), 111: (6, 9), 112: (6, 10), 113: (6, 11),
            114: (6, 12), 115: (6, 13), 116: (6, 14), 117: (6, 15), 118: (6, 17)
        }
    
    def create_element_button(self, element, row, column):
        """Создание кнопки элемента"""
        button = ElementButton(element)
        color = self.get_category_color(element.category)
        
        button_style = f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid #333;
                border-radius: 5px;
                font-weight: bold;
                font-size: 10pt;
                padding: 2px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color_brightness(color, 40)};
                border: 3px solid #000;
            }}
        """
        button.setStyleSheet(button_style)
        
        button.clicked.connect(lambda: self.display_element_info(element))
        
        self.table_grid.addWidget(button, row, column)
        self.element_buttons[element.atomic_number] = button
    
    def get_category_color(self, category):
        """Получение цвета для категории элемента"""
        color_map = {
            "Щелочные металлы": "#FF6666",
            "Щелочноземельные металлы": "#FFDEAD",
            "Переходные металлы": "#FFC0C0",
            "Постпереходные металлы": "#CCCCCC",
            "Металлоиды": "#CCFFCC",
            "Неметаллы": "#A0FFA0",
            "Галогены": "#FFFF99",
            "Инертные газы": "#C0FFFF",
            "Лантаноиды": "#FFBFFF",
            "Актиноиды": "#FF99CC"
        }
        return color_map.get(category, "#FFFFFF")
    
    def adjust_color_brightness(self, color, adjustment):
        """Корректировка яркости цвета"""
        if color.startswith("#"):
            red = int(color[1:3], 16)
            green = int(color[3:5], 16)
            blue = int(color[5:7], 16)
            
            red = min(255, red + adjustment)
            green = min(255, green + adjustment)
            blue = min(255, blue + adjustment)
            
            return f"#{red:02x}{green:02x}{blue:02x}"
        return color
    
    def create_search_panel(self):
        """Создание панели поиска"""
        search_group = QGroupBox("Поиск химического элемента")
        search_layout = QHBoxLayout()
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Название, символ или номер элемента...")
        self.search_field.textChanged.connect(self.highlight_matching_elements)
        search_layout.addWidget(self.search_field)
        
        self.category_selector = QComboBox()
        categories = ["Все категории"] + sorted(list(set(
            [elem.category for elem in self.element_database.all_elements]
        )))
        self.category_selector.addItems(categories)
        self.category_selector.currentTextChanged.connect(self.filter_elements_by_category)
        search_layout.addWidget(self.category_selector)
        
        search_group.setLayout(search_layout)
        return search_group
    
    def create_info_panel(self):
        """Создание панели информации"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        info_container = QWidget()
        info_layout = QVBoxLayout()
        
        self.current_element_label = QLabel("Выберите элемент для просмотра информации")
        self.current_element_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_element_label.setStyleSheet("font-size: 14pt; color: #666; margin: 20px;")
        info_layout.addWidget(self.current_element_label)
        
        self.detailed_info_display = QTextEdit()
        self.detailed_info_display.setReadOnly(True)
        info_layout.addWidget(self.detailed_info_display)
        
        info_container.setLayout(info_layout)
        scroll_area.setWidget(info_container)
        return scroll_area
    
    def display_element_info(self, element):
        """Отображение информации об элементе"""
        info_html = self.generate_element_info_html(element)
        self.detailed_info_display.setHtml(info_html)
        self.current_element_label.setText(f"{element.name} ({element.symbol})")
    
    def generate_element_info_html(self, element):
        """Генерация HTML с информацией об элементе"""
        melting_point = f"{element.melting_temperature} °C" if element.melting_temperature != "Неизвестно" else "Неизвестно"
        boiling_point = f"{element.boiling_temperature} °C" if element.boiling_temperature != "Неизвестно" else "Неизвестно"
        electronegativity = f"{element.electronegativity}" if element.electronegativity != "Неизвестно" else "Неизвестно"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="background-color: {self.get_category_color(element.category)}; 
                       padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 48px; color: #333;">{element.symbol}</h1>
                <h2 style="margin: 10px 0; color: #333;">{element.name}</h2>
                <h3 style="margin: 0; color: #666;">Атомный номер: {element.atomic_number}</h3>
            </div>
            
            <div style="margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse; font-size: 11pt;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold; width: 40%;">Атомная масса:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.atomic_mass} г/моль</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Группа:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.group}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Период:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.period}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Категория:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.category}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Электронная конфигурация:</td><td style="padding: 8px; border-bottom: 1px solid #ddd; font-family: monospace;">{element.electron_config}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Электроотрицательность:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{electronegativity}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Температура плавления:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{melting_point}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Температура кипения:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{boiling_point}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Плотность:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.density_value} г/см³</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Год открытия:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.year_discovered}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Первооткрыватель:</td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{element.discoverer_name}</td></tr>
                </table>
            </div>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #333;">📖 Интересные факты:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    {"".join([f"<li style='margin-bottom: 5px;'>{fact}</li>" for fact in element.interesting_facts])}
                </ul>
            </div>
            
            <div style="background-color: #e8f4fd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #333;">🏭 Применение:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    {"".join([f"<li style='margin-bottom: 5px;'>{use}</li>" for use in element.common_uses])}
                </ul>
            </div>
            
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0; color: #333;">📝 Описание:</h4>
                <p style="margin: 0; line-height: 1.6;">{element.element_description}</p>
            </div>
        </div>
        """
        return html_content
    
    def highlight_matching_elements(self):
        """Подсветка элементов, соответствующих поисковому запросу"""
        search_text = self.search_field.text().lower()
        
        for element in self.element_database.all_elements:
            button = self.element_buttons.get(element.atomic_number)
            if button:
                is_match = (search_text in element.name.lower() or 
                          search_text in element.symbol.lower() or
                          search_text in str(element.atomic_number))
                
                current_color = self.get_category_color(element.category)
                if search_text and is_match:
                    border_style = "3px solid #FF0000"
                else:
                    border_style = "2px solid #333"
                
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {current_color};
                        border: {border_style};
                        border-radius: 5px;
                        font-weight: bold;
                        font-size: 10pt;
                        padding: 2px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.adjust_color_brightness(current_color, 40)};
                        border: 3px solid #000;
                    }}
                """)
    
    def filter_elements_by_category(self):
        """Фильтрация элементов по категории"""
        selected_category = self.category_selector.currentText()
        
        for element in self.element_database.all_elements:
            button = self.element_buttons.get(element.atomic_number)
            if button:
                if selected_category == "Все категории" or element.category == selected_category:
                    button.setVisible(True)
                else:
                    button.setVisible(False)

class ChemistryTableApp(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Химическая таблица элементов")
        self.setGeometry(100, 100, 1600, 900)
        
        central_widget = PeriodicTableView()
        self.setCentralWidget(central_widget)

def launch_application():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    main_window = ChemistryTableApp()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    launch_application()