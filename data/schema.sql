CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    user_level INTEGER DEFAULT 1,
    accumulated_experience INTEGER DEFAULT 0,
    registration_date TEXT NOT NULL,
    correct_streak INTEGER DEFAULT 0,
    maximum_streak INTEGER DEFAULT 0,
    avatar_filename TEXT
);

CREATE TABLE IF NOT EXISTS achievements (
    achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    points INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_achievements (
    user_achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    unlock_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id),
    UNIQUE(user_id, achievement_id)
);

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
);

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
);

CREATE TABLE IF NOT EXISTS element_facts (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    atomic_number INTEGER NOT NULL,
    fact_text TEXT NOT NULL,
    FOREIGN KEY (atomic_number) REFERENCES elements(atomic_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS element_uses (
    use_id INTEGER PRIMARY KEY AUTOINCREMENT,
    atomic_number INTEGER NOT NULL,
    use_text TEXT NOT NULL,
    FOREIGN KEY (atomic_number) REFERENCES elements(atomic_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    question_type TEXT DEFAULT 'multiple_choice',
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    difficulty TEXT,
    points INTEGER DEFAULT 7,
    UNIQUE(question_text, correct_answer)
);

CREATE TABLE IF NOT EXISTS question_options (
    option_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS question_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    category_name TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_quiz_results_user ON quiz_results(user_id);
CREATE INDEX IF NOT EXISTS idx_elements_symbol ON elements(symbol);
CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_element_facts_number ON element_facts(atomic_number);
CREATE INDEX IF NOT EXISTS idx_element_uses_number ON element_uses(atomic_number);
CREATE INDEX IF NOT EXISTS idx_question_options ON question_options(question_id);
CREATE INDEX IF NOT EXISTS idx_question_categories ON question_categories(question_id);