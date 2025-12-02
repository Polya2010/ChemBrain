import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QMessageBox,
    QStackedWidget
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QKeySequence, QShortcut

from element_data_repository import ElementDataRepository
from periodic_table_view import PeriodicTableView
from quiz_content_manager import QuizContentManager
from quiz_interface import QuizInterface
from user_account_manager import UserAccountManager
from user_profile_screen import UserProfileScreen
from user_authentication_dialog import UserAuthenticationDialog

class ChemistryLearningApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemBrain - Изучение химии (Горячие клавиши: Ctrl+M, Ctrl+W, Ctrl+S, Ctrl+R, Ctrl+P, F11)")
        self.setGeometry(100, 100, 1400, 900)
        
        self.user_account_manager = UserAccountManager()
        self.element_data_repository = ElementDataRepository()
        
        self.central_navigation_widget = QStackedWidget()
        self.setCentralWidget(self.central_navigation_widget)
        
        self.initialize_main_application_interface()
        self.setup_hotkeys()
        self.display_authentication_dialog()
        
        # Переменная для отслеживания полноэкранного режима
        self.is_fullscreen = False
        # Переменная для хранения предыдущих размеров окна
        self.previous_geometry = None
    
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
    
    def setup_hotkeys(self):
        """Настройка горячих клавиш"""
        # Основные горячие клавиши
        shortcut_table = QShortcut(QKeySequence("Ctrl+M"), self)
        shortcut_table.activated.connect(self.switch_to_periodic_table)
        
        shortcut_quiz = QShortcut(QKeySequence("Ctrl+W"), self)
        shortcut_quiz.activated.connect(self.start_quiz)
        
        shortcut_stats = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_stats.activated.connect(self.switch_to_profile)
        
        # Управление элементами
        shortcut_random = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut_random.activated.connect(self.show_random_element)
        
        shortcut_print = QShortcut(QKeySequence("Ctrl+P"), self)
        shortcut_print.activated.connect(self.print_element_info)
        
        # Полноэкранный режим
        shortcut_fullscreen = QShortcut(QKeySequence("F11"), self)
        shortcut_fullscreen.activated.connect(self.toggle_fullscreen)
        
        # Дополнительные горячие клавиши
        shortcut_exit = QShortcut(QKeySequence("Ctrl+Q"), self)
        shortcut_exit.activated.connect(self.close)
        
        shortcut_help = QShortcut(QKeySequence("F1"), self)
        shortcut_help.activated.connect(self.show_help)
    
    def switch_to_periodic_table(self):
        """Переключение на вкладку таблицы Менделеева"""
        tab_widget = self.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(0)
    
    def start_quiz(self):
        """Запуск викторины"""
        tab_widget = self.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(1)
            
            if self.user_account_manager.active_user:
                QTimer.singleShot(100, self.quiz_interface._start_quiz_session)
            else:
                QMessageBox.information(self, "Авторизация", "Для прохождения викторины необходимо войти в систему")
    
    def switch_to_profile(self):
        """Переключение на вкладку профиля"""
        tab_widget = self.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(2)
            QTimer.singleShot(50, self.user_profile_interface.update_profile_display)
    
    def show_random_element(self):
        """Показать случайный элемент (Ctrl+R)"""
        self.switch_to_periodic_table()
        QTimer.singleShot(100, lambda: self.periodic_table_interface.show_random_element())
    
    def print_element_info(self):
        """Печать информации об элементе (Ctrl+P)"""
        if hasattr(self.periodic_table_interface, 'current_element') and self.periodic_table_interface.current_element:
            element = self.periodic_table_interface.current_element
            
            # Создаем принтер и диалог печати
            from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt6.QtGui import QTextDocument
            
            printer = QPrinter()
            print_dialog = QPrintDialog(printer, self)
            
            if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Получаем HTML контент
                html_content = self.periodic_table_interface._generate_detailed_information_html(element)
                
                # Создаем текстовый документ для печати
                document = QTextDocument()
                document.setHtml(html_content)
                
                # Печатаем документ
                document.print_(printer)
                
                QMessageBox.information(self, "Печать", "Информация об элементе отправлена на печать.")
        else:
            QMessageBox.warning(self, "Печать", "Сначала выберите элемент для печати информации.")
    
    def toggle_fullscreen(self):
        """Полноэкранный режим (F11)"""
        if not self.is_fullscreen:
            # Сохраняем текущие размеры окна
            self.previous_geometry = self.geometry()
            
            # Переходим в полноэкранный режим
            self.showFullScreen()
            self.is_fullscreen = True
        else:
            # Возвращаемся к обычному режиму
            self.showNormal()
            if self.previous_geometry:
                self.setGeometry(self.previous_geometry)
            self.is_fullscreen = False
    
    def show_help(self):
        """Показать справку по горячим клавишам"""
        help_text = """
        Горячие клавиши ChemBrain:
        
        Основные:
        Ctrl+M - Таблица Менделеева
        Ctrl+W - Викторина
        Ctrl+S - Профиль
        
        Управление элементами:
        Ctrl+R - Случайный элемент
        Ctrl+P - Печать информации об элементе
        
        Интерфейс:
        F11 - Полноэкранный режим
        Ctrl+Q - Выход
        F1 - Справка
        """
        
        QMessageBox.information(self, "Справка по горячим клавишам", help_text)
    
    def on_tab_changed(self, index):
        """Обработчик смены вкладок - обновляет профиль при переходе на вкладку профиля"""
        if index == 2:
            self.user_profile_interface.update_profile_display()
    
    def display_authentication_dialog(self):
        auth_dialog = UserAuthenticationDialog(self.user_account_manager)
        if auth_dialog.exec() == UserAuthenticationDialog.DialogCode.Accepted:
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