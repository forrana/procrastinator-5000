DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS record;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE activity (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  score INTEGER DEFAULT 1,
  icon BLOB,
  user_id INTEGER,
  category_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  is_positive BOOLEAN DEFAULT FALSE,
  description TEXT,
  icon BLOB,
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TIMESTAMP,
  title TEXT,
  description TEXT,
  is_active BOOLEAN DEFAULT FALSE,
  user_id INTEGER NOT NULL,
  activity_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (activity_id) REFERENCES activity (id)
);