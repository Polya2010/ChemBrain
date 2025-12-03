from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QProgressBar, QRadioButton, QButtonGroup, QTextEdit,
    QGroupBox, QComboBox, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
import random
from quiz_session import QuizAttempt


class QuizInteractionPanel(QWidget):
    def __init__(self, questions_manager, account_manager):
        super().__init__()
        self.questions_manager = questions_manager
        self.account_manager = account_manager
        self.active_attempt = None
        self.quiz_timer = QTimer()
        self.quiz_timer.timeout.connect(self._update_time_display)
        self.elapsed_seconds = 0
        self._initialize_interface()

    def _initialize_interface(self):
        main_layout = QVBoxLayout()

        header_label = QLabel("ВИКТОРИНА ПО ХИМИИ")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(
            "font-size: 16pt; font-weight: bold; margin: 10px;"
        )
        main_layout.addWidget(header_label)

        self.screen_container = QStackedWidget()

        self.selection_panel = self._create_selection_panel()
        self.screen_container.addWidget(self.selection_panel)

        self.quiz_panel = self._create_quiz_panel()
        self.screen_container.addWidget(self.quiz_panel)

        self.results_panel = self._create_results_panel()
        self.screen_container.addWidget(self.results_panel)

        main_layout.addWidget(self.screen_container)
        self.setLayout(main_layout)

        self._display_selection_panel()

    def _create_selection_panel(self):
        panel_widget = QWidget()
        panel_layout = QVBoxLayout()

        if self.account_manager.current_user:
            user_info_container = QGroupBox("Текущий пользователь")
            user_info_layout = QHBoxLayout()

            username = self.account_manager.current_user.user_name
            userlevel = self.account_manager.current_user.user_level
            userxp = self.account_manager.current_user.accumulated_experience

            user_info_layout.addWidget(QLabel(f"Пользователь: {username}"))
            user_info_layout.addWidget(QLabel(f"Уровень: {userlevel}"))
            user_info_layout.addWidget(QLabel(f"XP: {userxp}"))

            user_info_container.setLayout(user_info_layout)
            panel_layout.addWidget(user_info_container)

        settings_container = QGroupBox("Параметры викторины")
        settings_grid = QGridLayout()

        settings_grid.addWidget(QLabel("Тематика:"), 0, 0)
        self.category_selector = QComboBox()
        cat_items = ["Все", "Элементы", "Характеристики"]
        self.category_selector.addItems(cat_items)
        settings_grid.addWidget(self.category_selector, 0, 1)

        settings_grid.addWidget(QLabel("Сложность:"), 1, 0)
        self.difficulty_selector = QComboBox()
        diff_items = ["Любая", "Легкая", "Средняя", "Сложная"]
        self.difficulty_selector.addItems(diff_items)
        settings_grid.addWidget(self.difficulty_selector, 1, 1)

        settings_grid.addWidget(QLabel("Количество вопросов:"), 2, 0)
        self.quantity_selector = QComboBox()
        self.quantity_selector.addItems(["5", "10"])
        settings_grid.addWidget(self.quantity_selector, 2, 1)

        settings_container.setLayout(settings_grid)
        panel_layout.addWidget(settings_container)

        control_buttons = QHBoxLayout()

        self.start_quiz_button = QPushButton("Начать викторину")
        self.start_quiz_button.setStyleSheet("font-size: 12pt; padding: 10px;")
        self.start_quiz_button.clicked.connect(self._initiate_quiz)
        control_buttons.addWidget(self.start_quiz_button)

        panel_layout.addLayout(control_buttons)
        panel_widget.setLayout(panel_layout)
        return panel_widget

    def _create_quiz_panel(self):
        panel_widget = QWidget()
        panel_layout = QVBoxLayout()

        status_info = QHBoxLayout()

        self.progress_indicator = QProgressBar()
        self.progress_indicator.setMaximum(100)
        status_info.addWidget(QLabel("Прогресс:"))
        status_info.addWidget(self.progress_indicator)

        self.score_display = QLabel("Очки: 0")
        status_info.addWidget(self.score_display)

        self.time_display = QLabel("Время: 00:00")
        status_info.addWidget(self.time_display)

        panel_layout.addLayout(status_info)

        self.question_display = QLabel()
        self.question_display.setWordWrap(True)
        self.question_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_display.setStyleSheet("font-size: 12pt; margin: 15px;")
        panel_layout.addWidget(self.question_display)

        self.answers_container = QWidget()
        self.answers_layout = QVBoxLayout()
        self.answers_container.setLayout(self.answers_layout)
        panel_layout.addWidget(self.answers_container)

        navigation_controls = QHBoxLayout()

        self.next_question_button = QPushButton("Следующий вопрос")
        self.next_question_button.clicked.connect(self._proceed_to_next)
        navigation_controls.addWidget(self.next_question_button)

        self.finish_quiz_button = QPushButton("Завершить викторина")
        self.finish_quiz_button.clicked.connect(self._complete_quiz)
        navigation_controls.addWidget(self.finish_quiz_button)

        panel_layout.addLayout(navigation_controls)

        panel_widget.setLayout(panel_layout)
        return panel_widget

    def _create_results_panel(self):
        panel_widget = QWidget()
        panel_layout = QVBoxLayout()

        self.results_header = QLabel("Результаты викторины")
        self.results_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_header.setStyleSheet(
            "font-size: 16pt; font-weight: bold; margin: 10px;"
        )
        panel_layout.addWidget(self.results_header)

        self.results_summary = QLabel()
        self.results_summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_summary.setStyleSheet("font-size: 12pt; margin: 10px;")
        panel_layout.addWidget(self.results_summary)

        self.detailed_results = QTextEdit()
        self.detailed_results.setReadOnly(True)
        panel_layout.addWidget(self.detailed_results)

        action_buttons = QHBoxLayout()

        self.new_quiz_button = QPushButton("Новая викторина")
        self.new_quiz_button.clicked.connect(self._display_selection_panel)
        action_buttons.addWidget(self.new_quiz_button)

        panel_layout.addLayout(action_buttons)

        panel_widget.setLayout(panel_layout)
        return panel_widget

    def _display_selection_panel(self):
        self.screen_container.setCurrentWidget(self.selection_panel)

    def _initiate_quiz(self):
        try:
            if not self.account_manager.current_user:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Для участия в викторине требуется авторизация"
                )
                return

            category_mapping = {
                "Элементы": "elements",
                "Характеристики": "properties",
                "Все": "all",
                "Любая": "all"
            }
            difficulty_mapping = {
                "Легкая": "easy",
                "Средняя": "medium",
                "Сложная": "hard",
                "Любая": "all",
                "Все": "all"
            }

            selected_category = category_mapping.get(
                self.category_selector.currentText(),
                "all"
            )
            selected_difficulty = difficulty_mapping.get(
                self.difficulty_selector.currentText(),
                "all"
            )
            questions_amount = int(self.quantity_selector.currentText())

            print(f"Параметры викторины: категория={selected_category}, "
                  f"сложность={selected_difficulty}, "
                  f"количество={questions_amount}")

            question_list = self.questions_manager.get_filtered_questions(
                selected_category,
                selected_difficulty,
                questions_amount
            )

            if not question_list:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Вопросы по выбранным критериям не найдены!"
                )
                return

            print(f"Подготовлено {len(question_list)} вопросов")

            self.active_attempt = QuizAttempt(
                "Химическая викторина",
                question_list,
                self.account_manager
            )
            self.elapsed_seconds = 0
            self.quiz_timer.start(1000)

            self._show_current_question()
            self.screen_container.setCurrentWidget(self.quiz_panel)

        except Exception as error:
            print(f"Ошибка запуска викторины: {error}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка при запуске викторины: {str(error)}"
            )

    def _show_current_question(self):
        try:
            if not self.active_attempt:
                return

            current_question = self.active_attempt.get_active_question()
            if not current_question:
                self._complete_quiz()
                return

            progress_value = self.active_attempt.calculate_progress()
            self.progress_indicator.setValue(int(progress_value))
            score_text = f"Очки: {self.active_attempt.total_score}"
            self.score_display.setText(score_text)

            q_index = self.active_attempt.current_question_index + 1
            q_text = current_question.question_text
            question_text = f"Вопрос {q_index}: {q_text}"
            self.question_display.setText(question_text)

            self._clear_answer_options()

            if current_question.question_type == "multiple_choice":
                self._present_multiple_choice(current_question)
        except Exception as error:
            print(f"Ошибка отображения вопроса: {error}")

    def _clear_answer_options(self):
        for i in reversed(range(self.answers_layout.count())):
            widget_item = self.answers_layout.itemAt(i).widget()
            if widget_item:
                widget_item.deleteLater()

    def _present_multiple_choice(self, question_item):
        self.answer_options_group = QButtonGroup(self)

        answer_options = question_item.possible_answers.copy()
        random.shuffle(answer_options)

        for option_text in answer_options:
            option_button = QRadioButton(str(option_text))
            option_button.setStyleSheet("font-size: 11pt; padding: 8px;")
            self.answers_layout.addWidget(option_button)
            self.answer_options_group.addButton(option_button)

        submit_button = QPushButton("Ответить")
        submit_button.clicked.connect(self._process_selected_answer)
        self.answers_layout.addWidget(submit_button)

    def _process_selected_answer(self):
        try:
            selected_option = self.answer_options_group.checkedButton()
            if selected_option:
                user_answer = selected_option.text()
                self.active_attempt.process_user_response(user_answer)

                if self.active_attempt.completed:
                    self._complete_quiz()
                else:
                    self._show_current_question()
            else:
                QMessageBox.warning(
                    self,
                    "Внимание",
                    "Необходимо выбрать вариант ответа!"
                )
        except Exception as error:
            print(f"Ошибка обработки ответа: {error}")
            import traceback
            traceback.print_exc()

    def _proceed_to_next(self):
        try:
            if self.active_attempt:
                if not self.answer_options_group.checkedButton():
                    available_buttons = self.answer_options_group.buttons()
                    if available_buttons:
                        random.choice(available_buttons).setChecked(True)

                selected_option = self.answer_options_group.checkedButton()
                if selected_option:
                    self._process_selected_answer()
        except Exception as error:
            print(f"Ошибка перехода: {error}")

    def _complete_quiz(self):
        try:
            print("Завершение викторины...")
            self.quiz_timer.stop()

            if self.active_attempt and not self.active_attempt.completed:
                print("Завершение оставшихся вопросов...")
                while not self.active_attempt.completed:
                    self.active_attempt.process_user_response("")

                print("Финализация попытки...")
                quiz_results, unlocked_achievements, level_increased = (
                    self.active_attempt._finalize_quiz_attempt()
                )
                if quiz_results:
                    self.active_attempt.quiz_results = quiz_results
                    self.active_attempt.new_achievements = (
                        unlocked_achievements
                    )
                    self.active_attempt.level_increased = level_increased
                else:
                    print("Ошибка: результаты викторины отсутствуют")

            print("Отображение результатов...")
            self._present_final_results()
            self.screen_container.setCurrentWidget(self.results_panel)
            print("Результаты отображены")

        except Exception as error:
            print(f"КРИТИЧЕСКАЯ ОШИБКА завершения: {error}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка завершения викторины: {str(error)}"
            )

    def _present_final_results(self):
        try:
            if not self.active_attempt:
                print("Ошибка: активная попытка отсутствует")
                return

            current_attempt = self.active_attempt
            max_score = 0
            if current_attempt.question_set:
                max_score = sum(
                    q.score_value for q in current_attempt.question_set
                )

            success_percentage = 0
            if max_score > 0:
                success_percentage = (
                    current_attempt.total_score / max_score
                ) * 100

            correct_count = 0
            if current_attempt.answer_records:
                correct_count = sum(
                    1 for r in current_attempt.answer_records
                    if r['answer_correct']
                )

            correct_answers_text = (
                f"<p>Правильных ответов: {correct_count} из "
                f"{current_attempt.question_count}</p>"
            )
            time_spent = int(current_attempt.get_time_elapsed())
            time_text = f"<p>Затраченное время: {time_spent} секунд</p>"
            xp_gained = int(current_attempt.experience_gained)
            xp_text = f"<p>Полученный опыт: +{xp_gained} XP</p>"

            summary_text = f"""
            <h3>Викторина завершена!</h3>
            {correct_answers_text}
            <p>Набрано очков: {current_attempt.total_score} из {max_score}</p>
            <p>Результативность: {success_percentage:.1f}%</p>
            {time_text}
            {xp_text}
            """

            user_has_leveled_up = (
                hasattr(current_attempt, 'level_increased')
                and current_attempt.level_increased
                and self.account_manager.current_user
            )

            if user_has_leveled_up:
                level_msg = (
                    f"🎉 Достигнут уровень "
                    f"{self.account_manager.current_user.user_level}!"
                )
                summary_text += (
                    f"<p style='color: green; font-weight: bold;'>"
                    f"{level_msg}</p>"
                )

            has_new_achievements = (
                hasattr(current_attempt, 'new_achievements')
                and current_attempt.new_achievements
            )

            if has_new_achievements:
                achievements_text = (
                    "<p style='color: blue;'><b>Новые достижения:</b></p><ul>"
                )
                for achievement_item in current_attempt.new_achievements:
                    achievements_text += f"<li>{achievement_item['name']}</li>"
                achievements_text += "</ul>"
                summary_text += achievements_text

            self.results_summary.setText(summary_text)

            detailed_report = "<h4>Детализированные результаты:</h4><ul>"
            if current_attempt.answer_records:
                for idx, answer_record in enumerate(
                    current_attempt.answer_records,
                    1
                ):
                    is_correct = answer_record['answer_correct']
                    status = "✓ Верно" if is_correct else "✗ Неверно"
                    xp_info = ""
                    if is_correct:
                        xp_awarded = int(answer_record['experience_awarded'])
                        xp_info = f" (+{xp_awarded} XP)"
                    question_content = answer_record['question_content']
                    user_response = answer_record['user_response']
                    correct_response = answer_record['correct_response']
                    color_style = "green" if is_correct else "red"
                    color_text = f"<span style='color: {color_style}'>"
                    detailed_report += f"""
                    <li style="margin-bottom: 10px;">
                        <b>Вопрос {idx}:</b> {question_content}<br>
                        {color_text}
                            {status}{xp_info}
                        </span><br>
                        Ваш ответ: {user_response}<br>
                        Правильный ответ: {correct_response}
                    </li>
                    """
            detailed_report += "</ul>"
            self.detailed_results.setHtml(detailed_report)

        except Exception as error:
            print(f"Ошибка отображения результатов: {error}")
            import traceback
            traceback.print_exc()
            error_msg = f"Ошибка отображения результатов: {str(error)}"
            self.results_summary.setText(error_msg)

    def _update_time_display(self):
        self.elapsed_seconds += 1
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        time_text = f"Время: {minutes:02d}:{seconds:02d}"
        self.time_display.setText(time_text)
