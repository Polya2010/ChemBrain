import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from PyQt6.QtCore import QDateTime


class DatabaseManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            data_dir = os.path.join(parent_dir, "data")
            db_path = os.path.join(data_dir, "chemistry_app.db")

        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        db_exists = os.path.exists(self.db_path)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if not db_exists:
                schema_file = os.path.join(os.path.dirname(self.db_path), "schema.sql")
                if os.path.exists(schema_file):
                    with open(schema_file, "r", encoding="utf-8") as f:
                        schema_sql = f.read()
                    cursor.executescript(schema_sql)
                else:
                    self._create_tables(cursor)
            else:
                self._check_and_update_schema(cursor)

            conn.commit()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                user_level INTEGER DEFAULT 1,
                accumulated_experience INTEGER DEFAULT 0,
                registration_date TEXT NOT NULL,
                correct_streak INTEGER DEFAULT 0,
                maximum_streak INTEGER DEFAULT 0,
                avatar_filename TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                points INTEGER DEFAULT 0
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_achievements (
                user_achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                unlock_date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id),
                UNIQUE(user_id, achievement_id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quiz_title TEXT NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_responses INTEGER NOT NULL,
                final_score INTEGER NOT NULL,
                maximum_score INTEGER NOT NULL,
                time_elapsed_seconds INTEGER NOT NULL,
                experience_earned INTEGER NOT NULL,
                level_increased BOOLEAN DEFAULT 0,
                completed_date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS elements (
                atomic_number INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                name TEXT NOT NULL,
                atomic_weight REAL NOT NULL,
                element_group TEXT,
                period INTEGER,
                category TEXT,
                electron_config TEXT,
                electronegativity REAL,
                melting_point REAL,
                boiling_point REAL,
                density REAL,
                discovery_year TEXT,
                discoverer TEXT,
                description TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS element_facts (
                fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                atomic_number INTEGER NOT NULL,
                fact_text TEXT NOT NULL,
                FOREIGN KEY (atomic_number) REFERENCES elements(atomic_number) ON DELETE CASCADE
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS element_uses (
                use_id INTEGER PRIMARY KEY AUTOINCREMENT,
                atomic_number INTEGER NOT NULL,
                use_text TEXT NOT NULL,
                FOREIGN KEY (atomic_number) REFERENCES elements(atomic_number) ON DELETE CASCADE
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                question_type TEXT DEFAULT 'multiple_choice',
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                difficulty TEXT,
                points INTEGER DEFAULT 7,
                UNIQUE(question_text, correct_answer)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS question_options (
                option_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                option_text TEXT NOT NULL,
                is_correct BOOLEAN DEFAULT 0,
                FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS question_categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                category_name TEXT NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
            )
        """
        )

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_quiz_results_user ON quiz_results(user_id)"
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_elements_symbol ON elements(symbol)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_element_facts_number ON element_facts(atomic_number)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_element_uses_number ON element_uses(atomic_number)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_question_options ON question_options(question_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_question_categories ON question_categories(question_id)"
        )

    def _check_and_update_schema(self, cursor):
        try:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            )
            if not cursor.fetchone():
                self._create_tables(cursor)
        except Exception as e:
            print(f"Error checking database schema: {e}")

    def add_user(self, username: str) -> Optional[int]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                current_time = QDateTime.currentDateTime().toString(
                    "yyyy-MM-dd HH:mm:ss"
                )
                cursor.execute(
                    """
                    INSERT INTO users (username, registration_date)
                    VALUES (?, ?)
                """,
                    (username, current_time),
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        except Exception as e:
            print(f"Error adding user: {e}")
            return None

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
        except Exception as e:
            print(f"Error getting user: {e}")
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
        except Exception as e:
            print(f"Error getting user by id: {e}")
        return None

    def update_user_experience(self, user_id: int, experience: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users 
                    SET accumulated_experience = accumulated_experience + ?
                    WHERE user_id = ?
                """,
                    (experience, user_id),
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user experience: {e}")
            return False

    def update_user_level(self, user_id: int, new_level: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users 
                    SET user_level = ?
                    WHERE user_id = ?
                """,
                    (new_level, user_id),
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user level: {e}")
            return False

    def update_user_streak(self, user_id: int, correct: bool) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if correct:
                    cursor.execute(
                        """
                        UPDATE users 
                        SET correct_streak = correct_streak + 1,
                            maximum_streak = MAX(maximum_streak, correct_streak + 1)
                        WHERE user_id = ?
                    """,
                        (user_id,),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE users 
                        SET correct_streak = 0
                        WHERE user_id = ?
                    """,
                        (user_id,),
                    )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user streak: {e}")
            return False

    def save_quiz_result(self, user_id: int, quiz_data: Dict[str, Any]) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                current_time = QDateTime.currentDateTime().toString(
                    "yyyy-MM-dd HH:mm:ss"
                )
                cursor.execute(
                    """
                    INSERT INTO quiz_results 
                    (user_id, quiz_title, total_questions, correct_responses, 
                     final_score, maximum_score, time_elapsed_seconds, 
                     experience_earned, level_increased, completed_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        quiz_data.get("quiz_title", "Химическая викторина"),
                        quiz_data.get("total_questions", 0),
                        quiz_data.get("correct_responses", 0),
                        quiz_data.get("final_score", 0),
                        quiz_data.get("maximum_score", 0),
                        quiz_data.get("time_elapsed_seconds", 0),
                        quiz_data.get("experience_earned", 0),
                        1 if quiz_data.get("level_increased", False) else 0,
                        current_time,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving quiz result: {e}")
            return False

    def get_user_quiz_history(
        self, user_id: int, limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM quiz_results 
                    WHERE user_id = ? 
                    ORDER BY completed_date DESC 
                    LIMIT ?
                """,
                    (user_id, limit),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting user quiz history: {e}")
            return []

    def add_achievement(
        self, name: str, description: str = "", points: int = 0
    ) -> int:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO achievements (name, description, points)
                    VALUES (?, ?, ?)
                """,
                    (name, description, points),
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error adding achievement: {e}")
            return 0

    def unlock_achievement(self, user_id: int, achievement_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                current_time = QDateTime.currentDateTime().toString(
                    "yyyy-MM-dd HH:mm:ss"
                )
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO user_achievements (user_id, achievement_id, unlock_date)
                    VALUES (?, ?, ?)
                """,
                    (user_id, achievement_id, current_time),
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error unlocking achievement: {e}")
            return False

    def get_user_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT a.*, ua.unlock_date 
                    FROM achievements a
                    JOIN user_achievements ua ON a.achievement_id = ua.achievement_id
                    WHERE ua.user_id = ?
                    ORDER BY ua.unlock_date DESC
                """,
                    (user_id,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting user achievements: {e}")
            return []

    def get_all_achievements(self) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM achievements ORDER BY achievement_id")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting all achievements: {e}")
            return []

    def load_elements_from_json(
        self, elements_file: str, properties_file: str, additional_file: str
    ):
        try:
            with open(elements_file, "r", encoding="utf-8") as f:
                elements_data = json.load(f)

            with open(properties_file, "r", encoding="utf-8") as f:
                properties_data = json.load(f)

            with open(additional_file, "r", encoding="utf-8") as f:
                additional_data = json.load(f)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM element_facts")
                cursor.execute("DELETE FROM element_uses")
                cursor.execute("DELETE FROM elements")

                for element in elements_data.get("elements", []):
                    atomic_number = element["atomic_number"]
                    atomic_str = str(atomic_number)

                    props = properties_data.get("properties", {}).get(atomic_str, {})
                    additional = additional_data.get("additional_data", {}).get(
                        atomic_str, {}
                    )

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO elements 
                        (atomic_number, symbol, name, atomic_weight, element_group, 
                         period, category, electron_config, electronegativity, 
                         melting_point, boiling_point, density, discovery_year, 
                         discoverer, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            atomic_number,
                            element["symbol"],
                            element["name"],
                            element["atomic_weight"],
                            element["group"],
                            element["period"],
                            element["category"],
                            props.get("electron_config", ""),
                            props.get("electronegativity"),
                            props.get("melting_point"),
                            props.get("boiling_point"),
                            props.get("density"),
                            props.get("discovery_year", ""),
                            props.get("discoverer", ""),
                            props.get("description", ""),
                        ),
                    )

                    for fact in additional.get("facts", []):
                        cursor.execute(
                            """
                            INSERT INTO element_facts (atomic_number, fact_text)
                            VALUES (?, ?)
                        """,
                            (atomic_number, fact),
                        )

                    for use in additional.get("uses", []):
                        cursor.execute(
                            """
                            INSERT INTO element_uses (atomic_number, use_text)
                            VALUES (?, ?)
                        """,
                            (atomic_number, use),
                        )

                conn.commit()
                print(f"Loaded {len(elements_data['elements'])} elements into database")
                return True
        except Exception as e:
            print(f"Error loading elements: {e}")
            import traceback

            traceback.print_exc()
            return False

    def get_element_by_number(self, atomic_number: int) -> Optional[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM elements WHERE atomic_number = ?", (atomic_number,)
                )
                element = cursor.fetchone()
                if element:
                    element_dict = dict(element)
                    cursor.execute(
                        "SELECT fact_text FROM element_facts WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element_dict["facts"] = [row[0] for row in cursor.fetchall()]
                    cursor.execute(
                        "SELECT use_text FROM element_uses WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element_dict["uses"] = [row[0] for row in cursor.fetchall()]
                    return element_dict
        except Exception as e:
            print(f"Error getting element by number: {e}")
        return None

    def get_all_elements(self) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM elements ORDER BY atomic_number")
                elements = [dict(row) for row in cursor.fetchall()]

                for element in elements:
                    atomic_number = element["atomic_number"]
                    cursor.execute(
                        "SELECT fact_text FROM element_facts WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element["facts"] = [row[0] for row in cursor.fetchall()]
                    cursor.execute(
                        "SELECT use_text FROM element_uses WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element["uses"] = [row[0] for row in cursor.fetchall()]

                return elements
        except Exception as e:
            print(f"Error getting all elements: {e}")
            return []

    def search_elements(self, query: str) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                search_term = f"%{query.lower()}%"
                cursor.execute(
                    """
                    SELECT * FROM elements 
                    WHERE LOWER(name) LIKE ? 
                       OR LOWER(symbol) LIKE ?
                       OR CAST(atomic_number AS TEXT) LIKE ?
                    ORDER BY atomic_number
                """,
                    (search_term, search_term, search_term),
                )
                elements = [dict(row) for row in cursor.fetchall()]

                for element in elements:
                    atomic_number = element["atomic_number"]
                    cursor.execute(
                        "SELECT fact_text FROM element_facts WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element["facts"] = [row[0] for row in cursor.fetchall()]
                    cursor.execute(
                        "SELECT use_text FROM element_uses WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element["uses"] = [row[0] for row in cursor.fetchall()]

                return elements
        except Exception as e:
            print(f"Error searching elements: {e}")
            return []

    def get_elements_by_category(self, category: str) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM elements 
                    WHERE category = ?
                    ORDER BY atomic_number
                """,
                    (category,),
                )
                elements = [dict(row) for row in cursor.fetchall()]

                for element in elements:
                    atomic_number = element["atomic_number"]
                    cursor.execute(
                        "SELECT fact_text FROM element_facts WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element["facts"] = [row[0] for row in cursor.fetchall()]
                    cursor.execute(
                        "SELECT use_text FROM element_uses WHERE atomic_number = ?",
                        (atomic_number,),
                    )
                    element["uses"] = [row[0] for row in cursor.fetchall()]

                return elements
        except Exception as e:
            print(f"Error getting elements by category: {e}")
            return []

    def load_questions_from_json(self, questions_file: str):
        try:
            if not os.path.exists(questions_file):
                print(f"Файл с вопросами не найден: {questions_file}")
                return False

            with open(questions_file, "r", encoding="utf-8") as f:
                questions_data = json.load(f)

            questions = []

            if "questions" in questions_data:
                questions.extend(questions_data["questions"])

            if "basic_questions" in questions_data:
                questions.extend(questions_data["basic_questions"])

            if "supplementary_questions" in questions_data:
                questions.extend(questions_data["supplementary_questions"])

            if "element_questions" in questions_data:
                questions.extend(questions_data["element_questions"])

            if "extra_questions" in questions_data:
                questions.extend(questions_data["extra_questions"])

            if isinstance(questions_data, list):
                questions = questions_data

            if not questions:
                print(f"  В файле {questions_file} не найдено вопросов")
                return False

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                loaded_count = 0
                skipped_count = 0

                for q_data in questions:
                    cursor.execute(
                        "SELECT question_id FROM questions WHERE question_text = ? AND correct_answer = ?",
                        (q_data.get("question", ""), q_data.get("correct_answer", "")),
                    )

                    if cursor.fetchone():
                        skipped_count += 1
                        continue

                    try:
                        cursor.execute(
                            """
                            INSERT INTO questions 
                            (question_text, correct_answer, explanation, difficulty, points)
                            VALUES (?, ?, ?, ?, ?)
                        """,
                            (
                                q_data.get("question", ""),
                                q_data.get("correct_answer", ""),
                                q_data.get("explanation", ""),
                                q_data.get("difficulty", "Средняя"),
                                q_data.get("points", 7),
                            ),
                        )

                        question_id = cursor.lastrowid

                        options = q_data.get("options", [])
                        if options:
                            for option in options:
                                is_correct = option == q_data.get("correct_answer", "")
                                cursor.execute(
                                    """
                                    INSERT INTO question_options (question_id, option_text, is_correct)
                                    VALUES (?, ?, ?)
                                """,
                                    (question_id, option, 1 if is_correct else 0),
                                )

                        categories = q_data.get("category", [])
                        if isinstance(categories, str):
                            categories = [categories]

                        for category in categories:
                            cursor.execute(
                                """
                                INSERT INTO question_categories (question_id, category_name)
                                VALUES (?, ?)
                            """,
                                (question_id, category),
                            )

                        loaded_count += 1

                    except Exception as e:
                        print(f"    Ошибка при загрузке вопроса: {e}")
                        conn.rollback()
                        continue

                conn.commit()
                return loaded_count > 0

        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON файла {questions_file}: {e}")
            return False
        except Exception as e:
            print(f"Error loading questions from {questions_file}: {e}")
            import traceback

            traceback.print_exc()
            return False

    def get_questions(
        self, category: str = None, difficulty: str = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                query = """
                    SELECT DISTINCT q.* 
                    FROM questions q
                    LEFT JOIN question_categories qc ON q.question_id = qc.question_id
                    WHERE 1=1
                """
                params = []

                if category and category != "all":
                    query += " AND qc.category_name = ?"
                    params.append(category)

                if difficulty and difficulty != "all":
                    query += " AND q.difficulty = ?"
                    params.append(difficulty)

                query += " ORDER BY RANDOM() LIMIT ?"
                params.append(limit)

                cursor.execute(query, params)
                questions = []

                for row in cursor.fetchall():
                    question_dict = dict(row)
                    question_id = question_dict["question_id"]

                    cursor.execute(
                        "SELECT option_text FROM question_options WHERE question_id = ?",
                        (question_id,),
                    )
                    question_dict["options"] = [row[0] for row in cursor.fetchall()]

                    cursor.execute(
                        "SELECT category_name FROM question_categories WHERE question_id = ?",
                        (question_id,),
                    )
                    question_dict["categories"] = [row[0] for row in cursor.fetchall()]

                    questions.append(question_dict)

                return questions
        except Exception as e:
            print(f"Error getting questions: {e}")
            return []

    def get_question_count(self) -> int:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM questions")
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"Error getting question count: {e}")
            return 0

    def get_all_questions(self) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM questions ORDER BY question_id")
                questions = []

                for row in cursor.fetchall():
                    question_dict = dict(row)
                    question_id = question_dict["question_id"]

                    cursor.execute(
                        "SELECT option_text FROM question_options WHERE question_id = ?",
                        (question_id,),
                    )
                    question_dict["options"] = [row[0] for row in cursor.fetchall()]

                    cursor.execute(
                        "SELECT category_name FROM question_categories WHERE question_id = ?",
                        (question_id,),
                    )
                    question_dict["categories"] = [row[0] for row in cursor.fetchall()]

                    questions.append(question_dict)

                return questions
        except Exception as e:
            print(f"Error getting all questions: {e}")
            return []

    def get_all_categories(self) -> List[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT DISTINCT category_name FROM question_categories ORDER BY category_name"
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting all categories: {e}")
            return []

    def get_all_difficulties(self) -> List[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT DISTINCT difficulty FROM questions ORDER BY difficulty"
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting all difficulties: {e}")
            return []

    def backup_database(self, backup_path: str = None):
        if backup_path is None:
            backup_path = self.db_path + ".backup"

        try:
            import shutil

            shutil.copy2(self.db_path, backup_path)
            print(f"Database backed up to {backup_path}")
            return True
        except Exception as e:
            print(f"Error backing up database: {e}")
            return False

    def restore_database(self, backup_path: str):
        try:
            import shutil

            shutil.copy2(backup_path, self.db_path)
            print(f"Database restored from {backup_path}")
            return True
        except Exception as e:
            print(f"Error restoring database: {e}")
            return False

    def execute_sql(self, sql: str, params: tuple = None) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return False

    def execute_sql_file(self, sql_file: str) -> bool:
        try:
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_commands = f.read()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executescript(sql_commands)
                conn.commit()
            print(f"SQL file executed successfully: {sql_file}")
            return True
        except Exception as e:
            print(f"Error executing SQL file: {e}")
            return False

    def get_database_info(self) -> Dict[str, Any]:
        try:
            info = {"path": self.db_path, "size": 0, "tables": []}

            if os.path.exists(self.db_path):
                info["size"] = os.path.getsize(self.db_path)

                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                    )
                    tables = cursor.fetchall()

                    for table in tables:
                        table_name = table[0]
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        info["tables"].append({"name": table_name, "row_count": count})

            return info
        except Exception as e:
            print(f"Error getting database info: {e}")
            return {}

    def reset_database(self):
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                print(f"Database deleted: {self.db_path}")

            self._init_database()
            print("Database reinitialized")
            return True
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False