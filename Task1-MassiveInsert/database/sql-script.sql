CREATE TABLE IF NOT EXISTS user_counter(
	user_id  SERIAL PRIMARY KEY,
	counter INT,
	version INT);