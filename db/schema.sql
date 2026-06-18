CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT,
    telegram_id TEXT,
    current_level TEXT,
    manager_id INTEGER
);

CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    raw_transcript TEXT,
    summary TEXT,
    duration INTEGER,
    uploaded_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS video_skills (
    video_id INTEGER,
    skill_id INTEGER,
    PRIMARY KEY (video_id, skill_id)
);

CREATE TABLE IF NOT EXISTS user_skills (
    user_id INTEGER,
    skill_id INTEGER,
    proficiency_score REAL,
    PRIMARY KEY (user_id, skill_id)
);

CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER,
    title TEXT,
    questions_json TEXT
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    text TEXT,
    options_json TEXT,
    correct_index INTEGER
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    quiz_id INTEGER,
    score REAL,
    completed_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS learning_path_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path_id INTEGER,
    item_order INTEGER,
    item_type TEXT,
    item_id INTEGER,
    completed INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type TEXT,
    metadata_json TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
