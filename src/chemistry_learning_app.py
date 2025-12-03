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
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QKeySequence, QShortcut

from element_data_repository import ChemicalElementsStorage
from periodic_table_view import PeriodicTableDisplay
from quiz_content_manager import QuestionsManager
from quiz_interface import QuizInteractionPanel
from user_account_manager import AccountManager
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
        top_panel = QHBoxLayout()
        self.user_info_label = QLabel("Не авторизован")
        top_panel.addWidget(self.user_info_label)
        top_panel.addStretch()
        self.exit_button = QPushButton("Выйти")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6666;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                border: 1px solid #cc3333;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
            QPushButton:pressed {
                background-color: #cc0000;
            }
        """)
        self.exit_button.clicked.connect(self.close_application)
        top_panel.addWidget(self.exit_button)

        primary_layout.addLayout(top_panel)
        application_tabs = QTabWidget()

        self.periodic_table = PeriodicTableDisplay()
        application_tabs.addTab(self.periodic_table, "Таблица элементов")

        self.questions_manager = QuestionsManager(self.elements_storage)
        self.quiz_interface = QuizInteractionPanel(
            self.questions_manager,
            self.account_manager
        )
        application_tabs.addTab(self.quiz_interface, "Химические викторины")

        self.user_profile = UserProfileInterface(self.account_manager)
        application_tabs.addTab(self.user_profile, "Профиль пользователя")

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
        print_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        print_shortcut.activated.connect(self._print_element_data)
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

    def _print_element_data(self):
        if (
            hasattr(self.periodic_table, 'selected_element')
            and self.periodic_table.selected_element
        ):
            current_element = self.periodic_table.selected_element
            from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt6.QtGui import QTextDocument

            printing_device = QPrinter()
            print_dialog_window = QPrintDialog(
                printing_device,
                self,
            )

            if print_dialog_window.exec() == QPrintDialog.DialogCode.Accepted:
                html_content = self.periodic_table._generate_element_html(
                    current_element
                )
                printable_document = QTextDocument()
                printable_document.setHtml(html_content)
                printable_document.print_(printing_device)

                QMessageBox.information(
                    self,
                    "Печать",
                    "Информация об элементе отправлена на печать.",
                )
        else:
            QMessageBox.warning(
                self,
                "Печать",
                "Выберите элемент для печати информации",
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
                f"Пользователь: {active_user.user_name} | "
                f"Уровень: {active_user.user_level} | "
                f"XP: {active_user.accumulated_experience}"
            )
            self.user_profile.refresh_profile_data()
            self.exit_button.setVisible(True)
        else:
            self.user_info_label.setText("Не авторизован")
            self.exit_button.setVisible(False)
