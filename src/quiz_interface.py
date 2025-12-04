from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QProgressBar,
    QGridLayout,
    QComboBox,
    QSpinBox,
    QFrame,
    QTextEdit,
    QDialog,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import time


class QuizInteractionPanel(QWidget):
    def __init__(self, questions_manager, account_manager):
        super().__init__()
        self.questions_manager = questions_manager
        self.account_manager = account_manager
        self.current_questions = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.quiz_start_time = None
        self.user_answers = []
        self._initialize_ui()

    def _initialize_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("🧪 Химическая викторина")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        settings_group = QGroupBox("⚙️ Настройки викторины")
        settings_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #3498db;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
        )

        settings_layout = QGridLayout()
        settings_layout.setSpacing(10)

        cat_label = QLabel("📂 Категория:")
        cat_label.setStyleSheet("font-weight: bold;")
        settings_layout.addWidget(cat_label, 0, 0)

        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
        """
        )
        self.category_combo.addItem("📁 Все категории", "all")
        self.category_combo.addItem("⚛️ Элементы", "elements")
        self.category_combo.addItem("🔬 Свойства", "properties")
        self.category_combo.addItem("📜 История", "history")
        self.category_combo.addItem("🏭 Применение", "application")
        settings_layout.addWidget(self.category_combo, 0, 1)

        diff_label = QLabel("📈 Сложность:")
        diff_label.setStyleSheet("font-weight: bold;")
        settings_layout.addWidget(diff_label, 1, 0)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
        """
        )
        self.difficulty_combo.addItem("🎯 Любая", "all")
        self.difficulty_combo.addItem("😊 Легкая", "easy")
        self.difficulty_combo.addItem("😐 Средняя", "medium")
        self.difficulty_combo.addItem("🤯 Сложная", "hard")
        settings_layout.addWidget(self.difficulty_combo, 1, 1)

        count_label = QLabel("❓ Количество вопросов:")
        count_label.setStyleSheet("font-weight: bold;")
        settings_layout.addWidget(count_label, 2, 0)

        self.questions_combo = QComboBox()
        self.questions_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
        """
        )
        self.questions_combo.addItem("5 вопросов", 5)
        self.questions_combo.addItem("10 вопросов", 10)
        settings_layout.addWidget(self.questions_combo, 2, 1)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        self.start_button = QPushButton("🚀 Начать викторину")
        self.start_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 8px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """
        )
        self.start_button.clicked.connect(self._initiate_quiz)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.question_area = QGroupBox("📝 Вопрос")
        self.question_area.setVisible(False)
        self.question_area.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #9b59b6;
            }
        """
        )

        question_layout = QVBoxLayout()
        question_layout.setSpacing(10)

        self.question_info = QLabel("")
        self.question_info.setStyleSheet(
            "color: #7f8c8d; font-size: 12px; padding: 5px;"
        )
        question_layout.addWidget(self.question_info)

        self.question_text = QLabel("")
        self.question_text.setFont(QFont("Arial", 14))
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet(
            """
            QLabel {
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
            }
        """
        )
        question_layout.addWidget(self.question_text)

        self.options_group = QButtonGroup()
        self.options_group.setExclusive(True)
        self.options_layout = QVBoxLayout()
        self.options_layout.setSpacing(5)

        self.option_buttons = []
        for i in range(4):
            radio = QRadioButton()
            radio.setFont(QFont("Arial", 11))
            radio.setStyleSheet(
                """
                QRadioButton {
                    padding: 12px;
                    margin: 3px;
                    border-radius: 4px;
                    background-color: white;
                    border: 1px solid #ddd;
                }
                QRadioButton:hover {
                    background-color: #f0f7ff;
                    border-color: #3498db;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
            """
            )
            self.options_group.addButton(radio, i)
            self.options_layout.addWidget(radio)
            self.option_buttons.append(radio)

        question_layout.addLayout(self.options_layout)

        nav_layout = QHBoxLayout()

        self.prev_button = QPushButton("⬅️ Назад")
        self.prev_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        self.prev_button.clicked.connect(self._previous_question)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)

        nav_layout.addStretch()

        self.next_button = QPushButton("Далее ➡️")
        self.next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        self.next_button.clicked.connect(self._next_question)
        nav_layout.addWidget(self.next_button)

        question_layout.addLayout(nav_layout)

        self.question_area.setLayout(question_layout)
        main_layout.addWidget(self.question_area)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                height: 25px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """
        )
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.result_area = QGroupBox("🏆 Результат")
        self.result_area.setVisible(False)
        self.result_area.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #f39c12;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #f39c12;
            }
        """
        )

        result_layout = QVBoxLayout()
        result_layout.setSpacing(15)

        self.result_text = QLabel("")
        self.result_text.setFont(QFont("Arial", 12))
        self.result_text.setWordWrap(True)
        self.result_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_text.setStyleSheet("padding: 20px;")
        result_layout.addWidget(self.result_text)

        self.details_button = QPushButton("📊 Показать детали")
        self.details_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 6px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.details_button.clicked.connect(self._show_detailed_results)
        self.details_button.setVisible(False)

        self.restart_button = QPushButton("🔄 Пройти еще раз")
        self.restart_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 6px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        self.restart_button.clicked.connect(self._initiate_quiz)

        result_layout.addWidget(
            self.details_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        result_layout.addWidget(
            self.restart_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.result_area.setLayout(result_layout)
        main_layout.addWidget(self.result_area)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _initiate_quiz(self):
        if not self.account_manager.current_user:
            QMessageBox.warning(
                self, "Авторизация", "Для участия в викторине требуется вход в систему"
            )
            return

        category = self.category_combo.currentData()
        difficulty = self.difficulty_combo.currentData()
        questions_count = self.questions_combo.currentData()

        self.current_questions = self.questions_manager.get_filtered_questions(
            category, difficulty, questions_count
        )

        if not self.current_questions or len(self.current_questions) == 0:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не найдено вопросов по выбранным критериям!\nПопробуйте выбрать другие параметры.",
            )
            return

        self.current_question_index = 0
        self.correct_answers = 0
        self.user_answers = [None] * len(self.current_questions)
        self.quiz_start_time = time.time()

        self.start_button.setVisible(False)
        self.question_area.setVisible(True)
        self.progress_bar.setVisible(True)
        self.result_area.setVisible(False)
        self.details_button.setVisible(False)

        self.progress_bar.setMaximum(len(self.current_questions))
        self.progress_bar.setValue(1)

        self._display_current_question()

    def _display_current_question(self):
        if self.current_question_index >= len(self.current_questions):
            return

        question = self.current_questions[self.current_question_index]

        question_info = f"📋 Вопрос {self.current_question_index + 1} из {len(self.current_questions)}"
        question_info += f" | 📊 Сложность: {question.complexity_level}"
        if hasattr(question, "categories") and question.categories:
            question_info += f" | 📂 Категория: {', '.join(question.categories[:2])}"

        self.question_info.setText(question_info)

        self.question_text.setText(f"❓ {question.question_text}")

        self.options_group.setExclusive(False)
        for button in self.option_buttons:
            button.setChecked(False)
        self.options_group.setExclusive(True)

        for i, button in enumerate(self.option_buttons):
            if i < len(question.options):
                button.setText(f"{chr(65 + i)}. {question.options[i]}")
                button.setVisible(True)
                if (
                    self.user_answers[self.current_question_index]
                    == question.options[i]
                ):
                    button.setChecked(True)
            else:
                button.setVisible(False)

        self.prev_button.setEnabled(self.current_question_index > 0)

        if self.current_question_index == len(self.current_questions) - 1:
            self.next_button.setText("🏁 Завершить")
        else:
            self.next_button.setText("Далее ➡️")

        self.progress_bar.setValue(self.current_question_index + 1)
        self.progress_bar.setFormat(f"Прогресс: %v/%m (%p%)")

    def _previous_question(self):
        if self.current_question_index > 0:
            self._save_current_answer()
            self.current_question_index -= 1
            self._display_current_question()

    def _next_question(self):
        self._save_current_answer()

        if self.current_question_index < len(self.current_questions) - 1:
            self.current_question_index += 1
            self._display_current_question()
        else:
            self._finish_quiz()

    def _save_current_answer(self):
        checked_button = self.options_group.checkedButton()
        if checked_button:
            answer_text = checked_button.text()
            if ". " in answer_text:
                answer_text = answer_text.split(". ", 1)[1]
            self.user_answers[self.current_question_index] = answer_text
            return True
        self.user_answers[self.current_question_index] = None
        return False

    def _finish_quiz(self):
        self.correct_answers = 0
        self.detailed_results = []

        for i, question in enumerate(self.current_questions):
            user_answer = self.user_answers[i]
            is_correct = (
                user_answer == question.correct_answer if user_answer else False
            )
            if is_correct:
                self.correct_answers += 1

            self.detailed_results.append(
                {
                    "question": question.question_text,
                    "user_answer": user_answer,
                    "correct_answer": question.correct_answer,
                    "is_correct": is_correct,
                    "explanation": question.explanation,
                }
            )

        quiz_time = time.time() - self.quiz_start_time
        minutes = int(quiz_time // 60)
        seconds = int(quiz_time % 60)

        percentage = (
            (self.correct_answers / len(self.current_questions)) * 100
            if self.current_questions
            else 0
        )

        result_text = f"""
        <div style='text-align: center;'>
            <h2 style='color: #2c3e50;'>🏆 Викторина завершена!</h2>
            <p style='font-size: 16px;'><b>📊 Правильных ответов:</b> {self.correct_answers} из {len(self.current_questions)}</p>
            <p style='font-size: 16px;'><b>📈 Процент правильных ответов:</b> {percentage:.1f}%</p>
            <p style='font-size: 16px;'><b>⏱️ Затраченное время:</b> {minutes} мин {seconds} сек</p>
        """

        if percentage == 100:
            result_text += "<p style='color: #27ae60; font-size: 18px; font-weight: bold;'>🎉 Отлично! Идеальный результат!</p>"
        elif percentage >= 80:
            result_text += "<p style='color: #27ae60; font-size: 16px;'>👍 Отличный результат!</p>"
        elif percentage >= 60:
            result_text += "<p style='color: #f39c12; font-size: 16px;'>👌 Хороший результат!</p>"
        elif percentage >= 40:
            result_text += "<p style='color: #e67e22; font-size: 16px;'>😐 Можно лучше!</p>"
        else:
            result_text += "<p style='color: #e74c3c; font-size: 16px;'>📚 Попробуйте еще раз!</p>"

        result_text += "</div>"
        self.result_text.setText(result_text)

        quiz_result = {
            "quiz_title": "Химическая викторина",
            "total_questions": len(self.current_questions),
            "correct_responses": self.correct_answers,
            "final_score": int(percentage),
            "maximum_score": 100,
            "time_elapsed_seconds": int(quiz_time),
            "experience_earned": self.correct_answers * 10,
            "level_increased": False,
        }

        if self.account_manager.current_user:
            level_increased = self.account_manager.add_experience(
                quiz_result["experience_earned"]
            )
            quiz_result["level_increased"] = level_increased

            self.account_manager.save_quiz_result(quiz_result)

            for i in range(len(self.current_questions)):
                is_correct = (
                    self.user_answers[i] == self.current_questions[i].correct_answer
                )
                self.account_manager.update_streak_counter(is_correct)

            new_achievements = self.account_manager.check_achievement_progress(
                quiz_result
            )
            if new_achievements:
                achievements_text = "🎖️ Новые достижения:\n\n"
                for ach in new_achievements:
                    achievements_text += f"• {ach['name']} - {ach['description']}\n"
                QMessageBox.information(self, "🏆 Достижения", achievements_text)

        self.question_area.setVisible(False)
        self.progress_bar.setVisible(False)
        self.result_area.setVisible(True)
        self.details_button.setVisible(True)
        self.start_button.setVisible(True)

    def _show_detailed_results(self):
        if not hasattr(self, "detailed_results"):
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("📊 Детальные результаты")
        dialog.setMinimumSize(1000, 700)

        main_layout = QVBoxLayout(dialog)

        title_label = QLabel("📊 Детальные результаты викторины")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: #2c3e50; padding: 10px; text-align: center;"
        )
        main_layout.addWidget(title_label)

        stats_text = f"""
        <div style='text-align: center; background-color: #f8f9fa; padding: 10px; border-radius: 5px;'>
            <b>📊 Общая статистика:</b><br>
            Правильных ответов: {self.correct_answers} из {len(self.detailed_results)}<br>
            Процент правильных: {(self.correct_answers / len(self.detailed_results) * 100):.1f}%
        </div>
        """
        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Arial", 11))
        stats_label.setWordWrap(True)
        main_layout.addWidget(stats_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(15, 15, 15, 15)

        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(15)

        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(15)

        half_count = len(self.detailed_results) // 2
        if len(self.detailed_results) % 2 != 0:
            half_count += 1

        for i in range(half_count):
            result = self.detailed_results[i]
            question_widget = self._create_question_result_widget(i + 1, result)
            left_layout.addWidget(question_widget)

        for i in range(half_count, len(self.detailed_results)):
            result = self.detailed_results[i]
            question_widget = self._create_question_result_widget(i + 1, result)
            right_layout.addWidget(question_widget)

        left_layout.addStretch()
        right_layout.addStretch()

        container_layout.addWidget(left_column)
        container_layout.addWidget(right_column)

        scroll_area.setWidget(container)

        main_layout.addWidget(scroll_area)

        close_button = QPushButton("Закрыть")
        close_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 6px;
                font-size: 14px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        close_button.clicked.connect(dialog.accept)
        main_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.exec()

    def _create_question_result_widget(self, question_num, result):
        widget = QFrame()
        widget.setFrameShape(QFrame.Shape.Box)
        widget.setLineWidth(1)
        widget.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
            QFrame:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """
        )

        layout = QVBoxLayout(widget)
        layout.setSpacing(8)

        status_text = "✅ Правильно" if result["is_correct"] else "❌ Неправильно"
        status_color = "#27ae60" if result["is_correct"] else "#e74c3c"

        header_text = f"<b><span style='color: #2c3e50;'>Вопрос {question_num}:</span> <span style='color: {status_color};'>{status_text}</span></b>"
        header_label = QLabel(header_text)
        header_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_label.setWordWrap(True)
        layout.addWidget(header_label)

        question_text = f"<span style='color: #34495e;'>{result['question']}</span>"
        question_label = QLabel(question_text)
        question_label.setFont(QFont("Arial", 10))
        question_label.setWordWrap(True)
        question_label.setStyleSheet("margin-top: 5px;")
        layout.addWidget(question_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #ddd; margin: 10px 0;")
        layout.addWidget(separator)

        user_answer_text = (
            result["user_answer"] if result["user_answer"] else "Нет ответа"
        )
        user_answer_color = "#27ae60" if result["is_correct"] else "#e74c3c"
        user_answer_label = QLabel(
            f"<b>Ваш ответ:</b> <span style='color: {user_answer_color};'>{user_answer_text}</span>"
        )
        user_answer_label.setFont(QFont("Arial", 10))
        user_answer_label.setWordWrap(True)
        layout.addWidget(user_answer_label)

        correct_answer_label = QLabel(
            f"<b>Правильный ответ:</b> <span style='color: #27ae60;'>{result['correct_answer']}</span>"
        )
        correct_answer_label.setFont(QFont("Arial", 10))
        correct_answer_label.setWordWrap(True)
        layout.addWidget(correct_answer_label)

        if result["explanation"]:
            explanation_label = QLabel(
                f"<b>Пояснение:</b> <span style='color: #7f8c8d;'>{result['explanation']}</span>"
            )
            explanation_label.setFont(QFont("Arial", 9))
            explanation_label.setWordWrap(True)
            explanation_label.setStyleSheet(
                "margin-top: 5px; padding: 8px; background-color: #f8f9fa; border-radius: 4px;"
            )
            layout.addWidget(explanation_label)

        return widget