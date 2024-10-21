-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(70) UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    balance FLOAT
);

-- Create the 'stocks' table
CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    stock_price FLOAT NOT NULL,
    stock_name VARCHAR(40)
);

-- Create the 'transactions' table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    ticker_id INTEGER REFERENCES stocks(id) ON DELETE CASCADE,
    transaction_type VARCHAR(4) DEFAULT 'BUY',
    transaction_volume FLOAT NOT NULL,
    transaction_price FLOAT NOT NULL,
    created_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optionally, insert some initial data
-- INSERT INTO users (username, hashed_password, balance) VALUES ('test_user', 'hashed_password_here', 1000);
-- INSERT INTO stocks (ticker, stock_price, stock_name) VALUES ('AAPL', 150.00, 'Apple Inc.');
