# ПОЯСНИТЕЛЬНАЯ ЗАПИСКА
## К проекту "ChemBrain - Обучение химии"

### Описание проекта

**ChemBrain** - это интерактивное образовательное приложение для изучения химии, разработанное на Python с использованием библиотеки PyQt6. Приложение предоставляет пользователям комплексный инструмент для изучения периодической таблицы элементов, тестирования знаний через систему викторин и отслеживания прогресса обучения.

**Основные возможности:**
- Интерактивная таблица Менделеева с детальной информацией о каждом элементе
- Система химических викторин с вопросами разной сложности
- Управление пользовательскими профилями и достижениями
- Поиск элементов по различным критериям
- Система уровней и накопления опыта

### Структура проекта
ChemBrain/
├── data/                    # Папка с данными приложения
│   ├── __init__.py         # Инициализатор Python-пакета
│   ├── basic_questions.json # Базовые вопросы викторины
│   ├── chemistry_app.db    # База данных SQLite
│   ├── color_categories.json # Цветовая схема категорий элементов
│   ├── element_additional.json # Дополнительная информация об элементах
│   ├── element_positions.json # Координаты элементов в таблице
│   ├── element_properties.json # Свойства химических элементов
│   ├── element_quiz_questions.json # Вопросы об элементах
│   ├── element_template.html # HTML-шаблон для отображения элементов
│   ├── elements_data.json  # Основные данные об элементах
│   ├── extra_questions.json # Дополнительные вопросы
│   ├── initial_data.sql    # SQL-скрипт инициализации БД
│   ├── quiz_questions.json # Основные вопросы викторины
│   ├── schema.sql          # Схема базы данных
│   ├── supplementary_questions.json # Дополнительные вопросы
│   ├── user_progress_data.json # Данные о прогрессе пользователей
│   └── avatars/            # Папка с аватарками пользователей
├── src/                    # Исходный код приложения
│   ├── __init__.py        # Инициализатор Python-пакета
│   ├── chemical_element_data.py # Класс ElementInfo для данных элементов
│   ├── chemistry_learning_app.py # Главный класс приложения ChemistryEducationApp
│   ├── database_manager.py # Класс DatabaseManager для работы с БД
│   ├── element_interactive_button.py # Класс PeriodicTableButton
│   ├── help_content.py    # Контент справки
│   ├── help_manager.py    # Класс HelpManager для управления справкой
│   ├── main.py            # Точка входа в приложение
│   ├── modified_element_data_repository.py # Класс ChemicalElementsStorage
│   ├── modified_quiz_content_manager.py # Класс QuestionsManager
│   ├── modified_study_user.py # Класс LearningUser
│   ├── modified_user_account_manager.py # Класс AccountManager
│   ├── periodic_table_view.py # Класс PeriodicTableDisplay
│   ├── quiz_interface.py  # Класс QuizInteractionPanel
│   ├── quiz_question.py   # Класс QuestionItem
│   ├── quiz_session.py    # Класс QuizAttempt
│   ├── user_authentication_dialog.py # Класс LoginDialog
│   └── user_profile_screen.py # Класс UserProfileInterface
├── .gitignore            # Файл игнорирования Git
├── T3.md                # Дополнительные заметки по проекту
├── main.spec            # Конфигурация PyInstaller
├── README.md            # Основная документация проекта
└── requirements.txt     # Зависимости Python


### Детальное описание файлов

#### Папка `data/` - файлы данных

**JSON-файлы с данными элементов:**
- `elements_data.json` - основные характеристики 118 химических элементов (символы, названия, атомные номера, массы, группы, периоды, категории)
- `element_properties.json` - физико-химические свойства элементов (электронная конфигурация, электроотрицательность, температуры плавления/кипения, плотность)
- `element_additional.json` - интересные факты и области применения каждого элемента
- `color_categories.json` - цветовое кодирование категорий элементов для визуализации
- `element_positions.json` - координаты элементов в таблице Менделеева

**JSON-файлы с вопросами викторины:**
- `quiz_questions.json` - 10 основных вопросов викторины
- `basic_questions.json` - 5 базовых химических вопросов
- `element_quiz_questions.json` - 5 вопросов об элементах
- `extra_questions.json` - 100+ дополнительных вопросов
- `supplementary_questions.json` - 3 вспомогательных вопроса

**Файлы базы данных:**
- `chemistry_app.db` - SQLite база данных с таблицами пользователей, элементов, вопросов, результатов
- `schema.sql` - SQL-схема с CREATE TABLE командами
- `initial_data.sql` - начальные данные для БД (достижения, тестовый пользователь)

**Другие файлы:**
- `element_template.html` - HTML-шаблон для форматированного отображения информации об элементах
- `user_progress_data.json` - данные о прогрессе пользователей

#### Папка `src/` - исходный код

**Основные классы приложения:**
- `main.py` - точка входа, запускает QApplication и главное окно
- `chemistry_learning_app.py` - главный класс ChemistryEducationApp, управляет интерфейсом
- `database_manager.py` - класс DatabaseManager для работы с SQLite базой данных

**Классы для работы с химическими элементами:**
- `chemical_element_data.py` - класс ElementInfo для хранения данных об элементах
- `modified_element_data_repository.py` - класс ChemicalElementsStorage для управления данными элементов
- `periodic_table_view.py` - класс PeriodicTableDisplay для отображения таблицы Менделеева
- `element_interactive_button.py` - класс PeriodicTableButton для интерактивных кнопок элементов

**Классы для системы викторины:**
- `modified_quiz_content_manager.py` - класс QuestionsManager для управления вопросами
- `quiz_interface.py` - класс QuizInteractionPanel для интерфейса викторины
- `quiz_question.py` - класс QuestionItem для представления вопросов
- `quiz_session.py` - класс QuizAttempt для управления сессией викторины

**Классы для управления пользователями:**
- `modified_user_account_manager.py` - класс AccountManager для управления аккаунтами
- `modified_study_user.py` - класс LearningUser для представления пользователя
- `user_authentication_dialog.py` - класс LoginDialog для окна авторизации
- `user_profile_screen.py` - класс UserProfileInterface для экрана профиля

**Вспомогательные классы:**
- `help_content.py` - содержимое справки по горячим клавишам
- `help_manager.py` - класс HelpManager для отображения справки

### Инструкция по запуску программы

#### Требования к системе
- **Операционная система:** Windows 10/11, Linux, macOS
- **Python:** версия 3.8 или выше
- **ОЗУ:** не менее 2 ГБ
- **Дисковое пространство:** не менее 50 МБ

#### Шаги по установке и запуску

1. **Клонирование репозитория**
```bash
git clone <URL-репозитория>
cd ChemBrain