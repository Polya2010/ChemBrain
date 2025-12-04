import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QMessageBox,
    QStackedWidget,
    QComboBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QKeySequence, QShortcut

from modified_element_data_repository import ChemicalElementsStorage
from periodic_table_view import PeriodicTableDisplay
from modified_quiz_content_manager import QuestionsManager
from quiz_interface import QuizInteractionPanel
from modified_user_account_manager import AccountManager
from user_profile_screen import UserProfileInterface
from user_authentication_dialog import LoginDialog
from help_manager import HelpManager


class ChemistryEducationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemBrain - Обучение химии")
        self.setGeometry(100, 100, 1400, 900)

        self.account_manager = AccountManager()
        self.elements_storage = ChemicalElementsStorage()

        self.main_container = QStackedWidget()
        self.setCentralWidget(self.main_container)

        self._create_main_interface()
        self._configure_shortcuts()
        self.show_login_dialog()
        self.fullscreen_active = False
        self.previous_window_size = None

    def _create_main_interface(self):
        self.primary_widget = QWidget()
        primary_layout = QVBoxLayout()
        primary_layout.setContentsMargins(5, 5, 5, 5)
        primary_layout.setSpacing(5)
        
        top_panel = QHBoxLayout()
        top_panel.setContentsMargins(10, 5, 10, 5)
        
        self.user_info_label = QLabel("👤 Не авторизован")
        self.user_info_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                padding: 8px 15px;
                background-color: #ecf0f1;
                border-radius: 5px;
                border: 1px solid #bdc3c7;
            }
        """)
        top_panel.addWidget(self.user_info_label)
        
        top_panel.addStretch()
        
        self.exit_button = QPushButton("🚪 Выйти")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 5px;
                border: 1px solid #c0392b;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.exit_button.clicked.connect(self.close_application)
        self.exit_button.setVisible(False)
        top_panel.addWidget(self.exit_button)

        primary_layout.addLayout(top_panel)
        
        application_tabs = QTabWidget()
        application_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: white;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 10px 25px;
                margin-right: 3px;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
                color: #7f8c8d;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #3498db;
                border-bottom: 2px solid #3498db;
            }
            QTabBar::tab:hover {
                background-color: #dfe6e9;
                color: #2c3e50;
            }
        """)

        self.periodic_table = PeriodicTableDisplay()
        self.periodic_table.set_elements_storage(self.elements_storage)
        application_tabs.addTab(self.periodic_table, "📊 Таблица элементов")

        self.questions_manager = QuestionsManager(self.elements_storage)
        self.quiz_interface = QuizInteractionPanel(
            self.questions_manager,
            self.account_manager
        )
        application_tabs.addTab(self.quiz_interface, "🧪 Химические викторины")

        self.user_profile = UserProfileInterface(self.account_manager)
        application_tabs.addTab(self.user_profile, "👤 Профиль пользователя")

        application_tabs.currentChanged.connect(self._handle_tab_change)

        primary_layout.addWidget(application_tabs)
        self.primary_widget.setLayout(primary_layout)

        self.main_container.addWidget(self.primary_widget)

    def _configure_shortcuts(self):
        table_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        table_shortcut.activated.connect(self._navigate_to_table)
        
        quiz_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        quiz_shortcut.activated.connect(self._launch_quiz)
        
        profile_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        profile_shortcut.activated.connect(self._navigate_to_profile)
        
        random_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        random_shortcut.activated.connect(self._display_random_element)

        fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        fullscreen_shortcut.activated.connect(self._toggle_fullscreen)
        
        exit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        exit_shortcut.activated.connect(self.close_application)
        
        help_shortcut = QShortcut(QKeySequence("F1"), self)
        help_shortcut.activated.connect(
            lambda: HelpManager.show_help(self)
        )

    def close_application(self):
        reply = QMessageBox.question(
            self,
            "Выход из приложения",
            "Вы уверены, что хотите выйти из приложения?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    def _navigate_to_table(self):
        tab_widget = self.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(0)

    def _launch_quiz(self):
        tab_widget = self.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(1)

            if self.account_manager.current_user:
                QTimer.singleShot(100, self.quiz_interface._initiate_quiz)
            else:
                QMessageBox.information(
                    self,
                    "Авторизация",
                    "Для участия в викторине требуется вход в систему",
                )

    def _navigate_to_profile(self):
        tab_widget = self.findChild(QTabWidget)
        if tab_widget:
            tab_widget.setCurrentIndex(2)
            QTimer.singleShot(
                50,
                self.user_profile.refresh_profile_data,
            )

    def _display_random_element(self):
        self._navigate_to_table()
        QTimer.singleShot(
            100,
            lambda: self.periodic_table.display_random_element(),
        )

    def _toggle_fullscreen(self):
        if not self.fullscreen_active:
            self.previous_window_size = self.geometry()
            self.showFullScreen()
            self.fullscreen_active = True
        else:
            self.showNormal()
            if self.previous_window_size:
                self.setGeometry(self.previous_window_size)
            self.fullscreen_active = False

    def _handle_tab_change(self, selected_index):
        if selected_index == 2:
            self.user_profile.refresh_profile_data()

    def show_login_dialog(self):
        login_window = LoginDialog(self.account_manager)
        if login_window.exec() == LoginDialog.DialogCode.Accepted:
            self._update_interface_data()
            self.main_container.setCurrentWidget(self.primary_widget)
        else:
            self.close()

    def _update_interface_data(self):
        if self.account_manager.current_user:
            active_user = self.account_manager.current_user
            self.user_info_label.setText(
                f"👤 Пользователь: {active_user.user_name} | "
                f"📊 Уровень: {active_user.user_level} | "
                f"⭐ XP: {active_user.accumulated_experience}"
            )
            self.user_profile.refresh_profile_data()
            self.exit_button.setVisible(True)
        else:
            self.user_info_label.setText("👤 Не авторизован")
            self.exit_button.setVisible(False)