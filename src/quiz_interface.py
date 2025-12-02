from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QProgressBar, QRadioButton, QButtonGroup, QTextEdit,
    QGroupBox, QComboBox, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
import random
from quiz_session import QuizSession

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
        
        title = QLabel("ХИМИЧЕСКАЯ ВИКТОРИНА (Ctrl+W)")
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
        
        settings_layout.addWidget(QLabel("Количество вопросов:"), 2, 0)
        self.count_combo = QComboBox()
        self.count_combo.addItems(["5", "10"])
        settings_layout.addWidget(self.count_combo, 2, 1)
        
        settings.setLayout(settings_layout)
        layout.addWidget(settings)
        
        buttons = QHBoxLayout()
        
        self.start_btn = QPushButton("Начать викторину (Ctrl+W)")
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
        try:
            if not self.user_manager.active_user:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, войдите в систему для прохождения викторины")
                return
            
            category_map = {"Элементы": "elements", "Свойства": "properties", "Все": "all", "Любая": "all"}
            difficulty_map = {"Легкая": "easy", "Средняя": "medium", "Сложная": "hard", "Любая": "all", "Все": "all"}
            
            category = category_map.get(self.category_combo.currentText(), "all")
            difficulty = difficulty_map.get(self.difficulty_combo.currentText(), "all")
            count = int(self.count_combo.currentText())
            
            print(f"Запрос вопросов: категория={category}, сложность={difficulty}, количество={count}")
            
            questions = self.quiz_manager.retrieve_quiz_questions(category, difficulty, count)
            
            if not questions:
                QMessageBox.warning(self, "Ошибка", "Не найдено вопросов с выбранными критериями!")
                return
            
            print(f"Получено {len(questions)} вопросов для викторины")
            
            self.session = QuizSession("Химическая викторина", questions, self.user_manager)
            self.time_elapsed = 0
            self.timer.start(1000)
            
            self._display_current_question()
            self.screen_stack.setCurrentWidget(self.quiz_screen)
            
        except Exception as e:
            print(f"Ошибка при запуске викторины: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запуске викторины: {str(e)}")
    
    def _display_current_question(self):
        try:
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
        except Exception as e:
            print(f"Ошибка при отображении вопроса: {e}")
    
    def _clear_answer_options(self):
        for i in reversed(range(self.answers_layout.count())):
            widget = self.answers_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
    
    def _display_multiple_choice(self, question):
        self.buttons_group = QButtonGroup(self)
        
        # Перемешиваем варианты ответов
        options = question.answer_choices.copy()
        random.shuffle(options)
        
        for option in options:
            radio = QRadioButton(str(option))
            radio.setStyleSheet("font-size: 11pt; padding: 8px;")
            self.answers_layout.addWidget(radio)
            self.buttons_group.addButton(radio)
        
        submit_btn = QPushButton("Ответить")
        submit_btn.clicked.connect(self._submit_selected_answer)
        self.answers_layout.addWidget(submit_btn)
    
    def _submit_selected_answer(self):
        try:
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
        except Exception as e:
            print(f"Ошибка при отправке ответа: {e}")
            import traceback
            traceback.print_exc()
    
    def _next_question(self):
        try:
            if self.session:
                # Отмечаем случайный ответ если пользователь не выбрал
                if not self.buttons_group.checkedButton():
                    buttons = self.buttons_group.buttons()
                    if buttons:
                        random.choice(buttons).setChecked(True)
                
                selected = self.buttons_group.checkedButton()
                if selected:
                    self._submit_selected_answer()
        except Exception as e:
            print(f"Ошибка при переходе к следующему вопросу: {e}")
    
    def _finish_quiz(self):
        try:
            print("Завершение викторины...")
            self.timer.stop()
            
            if self.session and not self.session.done:
                print("Завершаем оставшиеся вопросы...")
                # Завершаем оставшиеся вопросы
                while not self.session.done:
                    self.session.submit_answer("")
                
                print("Завершаем сессию...")
                quiz_data, achievements, level_up = self.session._finalize_quiz_session()
                if quiz_data:
                    self.session.quiz_data = quiz_data
                    self.session.new_achievements = achievements
                    self.session.level_up = level_up
                else:
                    print("Ошибка: quiz_data is None")
            
            print("Отображаем результаты...")
            self._display_results()
            self.screen_stack.setCurrentWidget(self.results_screen)
            print("Результаты отображены")
            
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА при завершении викторины: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при завершении викторины: {str(e)}")
    
    def _display_results(self):
        try:
            if not self.session:
                print("Ошибка: сессия не существует")
                return
            
            session = self.session
            total_points = sum(q.point_value for q in session.questions) if session.questions else 0
            percentage = (session.score / total_points) * 100 if total_points > 0 else 0
            
            correct_answers = sum(1 for a in session.answers if a['is_correct']) if session.answers else 0
            
            summary = f"""
            <h3>Викторина завершена!</h3>
            <p>Правильных ответов: {correct_answers} из {session.total}</p>
            <p>Набрано очков: {session.score} из {total_points}</p>
            <p>Результат: {percentage:.1f}%</p>
            <p>Затраченное время: {int(session.get_elapsed_time())} секунд</p>
            <p>Получено опыта: +{int(session.xp_earned)} XP</p>
            """
            
            if hasattr(session, 'level_up') and session.level_up and self.user_manager.active_user:
                summary += f"<p style='color: green; font-weight: bold;'>🎉 Поздравляем! Вы достигли {self.user_manager.active_user.current_level} уровня!</p>"
            
            # Показываем новые достижения
            if hasattr(session, 'new_achievements') and session.new_achievements:
                achievements_text = "<p style='color: blue;'><b>Новые достижения:</b></p><ul>"
                for achievement in session.new_achievements:
                    achievements_text += f"<li>{achievement['name']}</li>"
                achievements_text += "</ul>"
                summary += achievements_text
            
            self.results_text.setText(summary)
            
            details = "<h4>Детальные результаты:</h4><ul>"
            if session.answers:
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
            
        except Exception as e:
            print(f"Ошибка при отображении результатов: {e}")
            import traceback
            traceback.print_exc()
            self.results_text.setText(f"Ошибка при отображении результатов: {str(e)}")
    
    def _update_timer_display(self):
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.time_label.setText(f"Время: {minutes:02d}:{seconds:02d}")