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
        self.elements_collection = self._initialize_elements_collection()
    
    def _initialize_elements_collection(self):
        element_records = [
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
        
        chemical_elements = []
        for record in element_records:
            element = ChemicalElementData(*record)
            self._enhance_element_data(element)
            chemical_elements.append(element)
        
        return chemical_elements
    
    def _enhance_element_data(self, element):
        properties = self._retrieve_element_properties(element.atomic_num)
        element.configure_physical_properties(*properties[:5])
        element.set_discovery_info(*properties[5:8])
        element.set_additional_data(*properties[8:])
    
    def _retrieve_element_properties(self, atomic_number):
        properties_database = {
            1: ("1s¹", 2.20, -259.16, -252.87, 0.0000899, 1766, "Генри Кавендиш", 
                "Самый легкий и распространенный элемент во Вселенной", 
                ["Составляет 75% массы Вселенной", "Первый элемент после Большого взрыва"],
                ["Производство аммиака", "Ракетное топливо", "Металлургия"]),
            2: ("1s²", None, -272.2, -268.93, 0.0001785, 1868, "Пьер Жансен", 
                "Второй по легкости элемент", 
                ["Используется в воздухоплавании", "Негорючий газ"],
                ["Дирижабли", "Криогеника", "Дыхательные смеси"]),
            3: ("[He] 2s¹", 0.98, 180.5, 1342, 0.534, 1817, "Йохан Арфведсон",
                "Щелочной металл",
                ["Плавает на воде", "Самый легкий металл"],
                ["Батареи", "Сплавы", "Психиатрия"]),
            6: ("[He] 2s² 2p²", 2.55, 3550, 4827, 2.267, "Древность", "Древние",
                "Основа органической химии",
                ["Образует алмаз и графит", "Имеет множество аллотропов"],
                ["Топливо", "Сталь", "Углеродные материалы"]),
            7: ("[He] 2s² 2p³", 3.04, -210.1, -195.8, 0.001251, 1772, "Даниэль Резерфорд",
                "Газ атмосферы",
                ["Составляет 78% воздуха", "Не поддерживает горение"],
                ["Удобрения", "Азотная кислота", "Промышленность"]),
            8: ("[He] 2s² 2p⁴", 3.44, -218.8, -183, 0.001429, 1774, "Карл Шееле",
                "Жизненно важный газ",
                ["Самый распространенный элемент в земной коре", "Поддерживает горение"],
                ["Дыхание", "Медицина", "Промышленность"]),
            11: ("[Ne] 3s¹", 0.93, 97.72, 883, 0.968, 1807, "Хемфри Дэви",
                 "Щелочной металл",
                 ["Шестой по распространенности элемент", "Очень реакционноспособный"],
                 ["Освещение", "Металлургия", "Производство мыла"]),
            13: ("[Ne] 3s² 3p¹", 1.61, 660.32, 2519, 2.70, 1825, "Ханс Эрстед",
                 "Легкий металл",
                 ["Самый распространенный металл в земной коре", "Устойчив к коррозии"],
                 ["Авиация", "Упаковка", "Электроника"]),
            14: ("[Ne] 3s² 3p²", 1.90, 1414, 3265, 2.33, 1824, "Йёнс Якоб Берцелиус",
                 "Полупроводник",
                 ["Второй по распространенности элемент", "Основной компонент песка"],
                 ["Электроника", "Стекло", "Солнечные панели"]),
            17: ("[Ne] 3s² 3p⁵", 3.16, -101.5, -34.04, 0.003214, 1774, "Карл Шееле",
                 "Желто-зеленый газ",
                 ["Образует поваренную соль", "Сильный окислитель"],
                 ["Дезинфекция", "Пластмассы", "Фармацевтика"]),
            19: ("[Ar] 4s¹", 0.82, 63.5, 759, 0.856, 1807, "Хемфри Дэви",
                 "Щелочной металл",
                 ["Седьмой по распространенности элемент", "Важен для живых организмов"],
                 ["Удобрения", "Медицина", "Пищевая промышленность"]),
            20: ("[Ar] 4s²", 1.00, 842, 1484, 1.55, 1808, "Хемфри Дэви",
                 "Щелочноземельный металл",
                 ["Пятый по распространенности элемент", "Основа костей"],
                 ["Строительство", "Медицина", "Производство цемента"]),
            26: ("[Ar] 3d⁶ 4s²", 1.83, 1538, 2862, 7.87, "Древность", "Древние",
                 "Важнейший металл",
                 ["Второй по распространенности металл", "Основной компонент стали"],
                 ["Машиностроение", "Строительство", "Транспорт"]),
            29: ("[Ar] 3d¹⁰ 4s¹", 1.90, 1084.62, 2562, 8.96, "Древность", "Древние",
                 "Цветной металл",
                 ["Хороший проводник", "Первый металл, использованный человеком"],
                 ["Электротехника", "Строительство", "Ювелирные изделия"]),
            47: ("[Kr] 4d¹⁰ 5s¹", 1.93, 961.78, 2162, 10.49, "Древность", "Древние",
                 "Благородный металл",
                 ["Лучший проводник электричества", "Используется в фотографии"],
                 ["Ювелирные изделия", "Электроника", "Медицина"]),
            79: ("[Xe] 4f¹⁴ 5d¹⁰ 6s¹", 2.54, 1064.18, 2856, 19.32, "Древность", "Древние",
                 "Благородный металл",
                 ["Не окисляется на воздухе", "Самый ковкий металл"],
                 ["Ювелирные изделия", "Электроника", "Финансы"]),
        }
        
        default_properties = ("Неизвестно", "Неизвестно", "Неизвестно", "Неизвестно", 
                             "Неизвестно", "Неизвестно", "Неизвестно", "Описание элемента",
                             ["Интересный факт"], ["Применение элемента"])
        
        return properties_database.get(atomic_number, default_properties)

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
        element_positions = self._get_element_grid_positions()
        
        for element in self.data_repository.elements_collection:
            if element.atomic_num in element_positions:
                row, column = element_positions[element.atomic_num]
                self._create_element_button(element, row, column)
    
    def _get_element_grid_positions(self):
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
        color_mapping = {
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
        melting_temp = f"{element.melting_point}°C" if element.melting_point != "Неизвестно" else "Неизвестно"
        boiling_temp = f"{element.boiling_point}°C" if element.boiling_point != "Неизвестно" else "Неизвестно"
        electronegativity = f"{element.electronegativity_val}" if element.electronegativity_val != "Неизвестно" else "Неизвестно"
        
        html_content = f"""
        <div style="font-family: Arial; line-height: 1.6;">
            <div style="background: {self._determine_category_color(element.classification)}; 
                       padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 15px;">
                <h1 style="margin: 0; font-size: 36px;">{element.symbol}</h1>
                <h2 style="margin: 5px 0; color: #333;">{element.full_name}</h2>
                <h3 style="margin: 0; color: #666;">Атомный номер: {element.atomic_num}</h3>
            </div>
            
            <table style="width: 100%; border-collapse: collapse; font-size: 10pt;">
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold; width: 40%;">Атомная масса:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.weight}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Группа:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.group_num}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Период:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.period_num}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Категория:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.classification}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Электронная конфигурация:</td><td style="padding: 6px; border-bottom: 1px solid #ddd; font-family: monospace;">{element.electron_config}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Электроотрицательность:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{electronegativity}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Температура плавления:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{melting_temp}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Температура кипения:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{boiling_temp}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Плотность:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.density_val}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Год открытия:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.discovery_year}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd; font-weight: bold;">Первооткрыватель:</td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{element.discoverer_info}</td></tr>
            </table>
            
            <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 10px 0;">
                <h4 style="margin-top: 0; color: #333;">📖 Интересные факты:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    {"".join([f"<li style='margin-bottom: 3px;'>{fact}</li>" for fact in element.interesting_facts_list])}
                </ul>
            </div>
            
            <div style="background: #e8f4fd; padding: 12px; border-radius: 6px;">
                <h4 style="margin-top: 0; color: #333;">🏭 Применение:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    {"".join([f"<li style='margin-bottom: 3px;'>{use}</li>" for use in element.common_uses_list])}
                </ul>
            </div>
            
            <div style="background: #f0f0f0; padding: 12px; border-radius: 6px; margin-top: 10px;">
                <h4 style="margin-top: 0; color: #333;">📝 Описание:</h4>
                <p style="margin: 0; line-height: 1.6;">{element.element_description}</p>
            </div>
        </div>
        """
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
    def __init__(self, question_text, question_format, answer_choices, correct_response, difficulty_level="medium", question_category="elements"):
        self.question_text = question_text
        self.question_format = question_format
        self.answer_choices = answer_choices
        self.correct_response = correct_response
        self.difficulty_level = difficulty_level
        self.question_category = question_category
        self.point_value = self._compute_point_value()
    
    def _compute_point_value(self):
        point_system = {"easy": 1, "medium": 2, "hard": 3}
        return point_system.get(self.difficulty_level, 1)
    
    def validate_answer(self, user_response):
        return str(user_response).strip().lower() == str(self.correct_response).strip().lower()

class QuizContentManager:
    def __init__(self, element_repository):
        self.element_repository = element_repository
        self.question_bank = self._generate_question_bank()
    
    def _generate_question_bank(self):
        questions_collection = []
        
        # Вопросы на символы элементов
        for element in self.element_repository.elements_collection:
            questions_collection.append(QuizQuestion(
                f"Какой символ у элемента '{element.full_name}'?",
                "multiple_choice",
                self._generate_incorrect_options(element.symbol, True),
                element.symbol,
                "easy",
                "elements"
            ))
        
        # Вопросы на атомные номера
        for element in self.element_repository.elements_collection[:50]:  # Первые 50 элементов
            questions_collection.append(QuizQuestion(
                f"Какой атомный номер у элемента {element.symbol}?",
                "multiple_choice",
                self._generate_incorrect_options(element.atomic_num, False),
                element.atomic_num,
                "easy",
                "elements"
            ))
        
        # Вопросы на названия элементов
        for element in self.element_repository.elements_collection[:30]:
            questions_collection.append(QuizQuestion(
                f"Как называется элемент с символом {element.symbol}?",
                "multiple_choice",
                self._generate_incorrect_names(element.full_name),
                element.full_name,
                "easy",
                "elements"
            ))
        
        # Общие вопросы по химии
        general_questions = [
            QuizQuestion(
                "Какой элемент имеет самую высокую электроотрицательность?",
                "multiple_choice",
                ["Кислород", "Фтор", "Хлор", "Азот"],
                "Фтор",
                "hard",
                "properties"
            ),
            QuizQuestion(
                "Самый распространенный элемент в земной коре?",
                "multiple_choice",
                ["Кислород", "Кремний", "Алюминий", "Железо"],
                "Кислород",
                "easy",
                "properties"
            ),
            QuizQuestion(
                "Какой элемент является основным компонентом органических соединений?",
                "multiple_choice",
                ["Водород", "Кислород", "Углерод", "Азот"],
                "Углерод",
                "medium",
                "properties"
            ),
            QuizQuestion(
                "Какой газ составляет около 78% атмосферы Земли?",
                "multiple_choice",
                ["Кислород", "Азот", "Аргон", "Углекислый газ"],
                "Азот",
                "easy",
                "properties"
            )
        ]
        questions_collection.extend(general_questions)
        
        return questions_collection
    
    def _generate_incorrect_options(self, correct_value, is_symbol):
        if is_symbol:
            all_options = [elem.symbol for elem in self.element_repository.elements_collection]
        else:
            all_options = [elem.atomic_num for elem in self.element_repository.elements_collection]
        
        incorrect_options = [opt for opt in all_options if opt != correct_value]
        
        if len(incorrect_options) >= 3:
            wrong_choices = random.sample(incorrect_options, 3)
        else:
            wrong_choices = incorrect_options
            while len(wrong_choices) < 3:
                if is_symbol:
                    fake_option = random.choice(["X", "Y", "Z", "W"])
                else:
                    fake_option = random.randint(1, 118)
                if fake_option not in wrong_choices and fake_option != correct_value:
                    wrong_choices.append(fake_option)
            
        all_choices = wrong_choices + [correct_value]
        random.shuffle(all_choices)
        return all_choices
    
    def _generate_incorrect_names(self, correct_name):
        all_names = [elem.full_name for elem in self.element_repository.elements_collection]
        incorrect_names = [name for name in all_names if name != correct_name]
        
        if len(incorrect_names) >= 3:
            wrong_choices = random.sample(incorrect_names, 3)
        else:
            wrong_choices = incorrect_names
            while len(wrong_choices) < 3:
                fake_names = ["Неон", "Аргон", "Криптон", "Ксенон", "Радон"]
                fake_name = random.choice(fake_names)
                if fake_name not in wrong_choices and fake_name != correct_name:
                    wrong_choices.append(fake_name)
            
        all_choices = wrong_choices + [correct_name]
        random.shuffle(all_choices)
        return all_choices
    
    def retrieve_quiz_questions(self, category_filter="all", difficulty_filter="all", question_count=5):
        try:
            filtered_questions = self.question_bank
            
            if category_filter != "all":
                filtered_questions = [q for q in filtered_questions if q.question_category == category_filter]
            
            if difficulty_filter != "all":
                filtered_questions = [q for q in filtered_questions if q.difficulty_level == difficulty_filter]
            
            if len(filtered_questions) > question_count:
                return random.sample(filtered_questions, question_count)
            else:
                return filtered_questions
        except Exception as e:
            print(f"Ошибка при получении вопросов: {e}")
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
    
    def _initialize_achievements(self):
        return [
            {'id': 1, 'name': 'Первые шаги', 'description': 'Пройти первую викторину'},
            {'id': 2, 'name': 'Серия удач', 'description': 'Ответить правильно на 10 вопросов подряд'},
            {'id': 4, 'name': 'Эрудит', 'description': 'Набрать 100% правильных ответов в викторине'},
            {'id': 7, 'name': 'Скорострел', 'description': 'Пройти викторину менее чем за 2 минуты'},
            {'id': 10, 'name': 'Менделеев нашего времени', 'description': 'Достичь 10 уровня'}
        ]
    
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
    
    def save_user_data(self):
        data_structure = {
            'users': [user.convert_to_dictionary() for user in self.registered_users],
            'achievements': self.available_achievements
        }
        try:
            with open('user_progress_data.json', 'w', encoding='utf-8') as file:
                json.dump(data_structure, file, ensure_ascii=False, indent=2)
        except Exception as error:
            print(f"Ошибка сохранения данных: {error}")
    
    def load_user_data(self):
        try:
            if os.path.exists('user_progress_data.json'):
                with open('user_progress_data.json', 'r', encoding='utf-8') as file:
                    loaded_data = json.load(file)
                    self.registered_users = [StudyUser.create_from_dictionary(user_data) for user_data in loaded_data.get('users', [])]
                    self.available_achievements = loaded_data.get('achievements', self.available_achievements)
        except Exception as error:
            print(f"Ошибка загрузки данных: {error}")
    
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
            
            self.answers.append({
                'question': current.question_text,
                'user_answer': answer,
                'correct': current.correct_response,
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
        
        accuracy = self.score / sum(q.point_value for q in self.questions)
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
        
        settings_layout.addWidget(QLabel("Вопросов:"), 2, 0)
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
            category_map = {"Элементы": "elements", "Свойства": "properties", "Все": "all"}
            difficulty_map = {"Легкая": "easy", "Средняя": "medium", "Сложная": "hard", "Любая": "all"}
            
            category = category_map.get(self.category_combo.currentText(), "all")
            difficulty = difficulty_map.get(self.difficulty_combo.currentText(), "all")
            count = int(self.count_combo.currentText())
            
            questions = self.quiz_manager.retrieve_quiz_questions(category, difficulty, count)
            
            if not questions:
                QMessageBox.warning(self, "Ошибка", "Не найдено вопросов с выбранными критериями!")
                return
            
            self.session = QuizSession("Химическая викторина", questions, self.user_manager)
            self.time_elapsed = 0
            self.timer.start(1000)
            
            self._display_current_question()
            self.screen_stack.setCurrentWidget(self.quiz_screen)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске викторины: {str(e)}")
    
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
        
        for option in question.answer_choices:
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
            # Пропускаем текущий вопрос
            self.session.submit_answer("")
            self._display_current_question()
    
    def _finish_quiz(self):
        self.timer.stop()
        if self.session and not self.session.done:
            quiz_data, achievements, level_up = self.session._finalize_quiz_session()
            self.session.quiz_data = quiz_data
            self.session.new_achievements = achievements
            self.session.level_up = level_up
            self.session.done = True
        
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
        
        if hasattr(session, 'level_up') and session.level_up:
            summary += f"<p style='color: green; font-weight: bold;'>🎉 Поздравляем! Вы достигли {self.user_manager.active_user.current_level} уровня!</p>"
        
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
        
        # Удалена кнопка "Профиль"
        
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
        
        # Добавляем обработчик смены вкладок
        application_tabs.currentChanged.connect(self.on_tab_changed)
        
        primary_layout.addWidget(application_tabs)
        self.main_interface_widget.setLayout(primary_layout)
        
        self.central_navigation_widget.addWidget(self.main_interface_widget)
    
    def on_tab_changed(self, index):
        """Обработчик смены вкладок - обновляет профиль при переходе на вкладку профиля"""
        if index == 2:  # Вкладка "Профиль" имеет индекс 2
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
            # Обновляем профиль при каждом обновлении интерфейса
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