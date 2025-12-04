INSERT OR IGNORE INTO achievements (name, description, points) VALUES 
('Начало пути', 'Пройти первую викторину', 0),
('Последовательность успеха', 'Ответить правильно на 10 вопросов подряд', 0),
('Знаток химии', 'Набрать 100% правильных ответов в викторине', 0),
('Молниеносный ответ', 'Пройти викторину менее чем за 2 минуты', 0),
('Современный Менделеев', 'Достичь 10 уровня', 0);

INSERT OR IGNORE INTO users (username, registration_date) VALUES 
('test_user', datetime('now'));