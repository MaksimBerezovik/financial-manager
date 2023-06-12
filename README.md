# Financial manager ver. 0.1
---
### Software version
- python: 3.10.8
- poetry: 1.5.1

### Getting started
To get started with this project, follow the steps below:
1. Create database with 2 tables SQLite.
```
CREATE TABLE records (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT
                       NOT NULL,
    user_id   INTEGER  REFERENCES users (id) ON DELETE CASCADE
                       NOT NULL,
    operation BOOLEAN  NOT NULL,
    value     DECIMAL  NOT NULL,
    date      DATETIME NOT NULL
                       DEFAULT ( (DATETIME('now') ) ),
    info      TEXT,
    [group]   TEXT
);
```
```
CREATE TABLE users (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER  UNIQUE
                       NOT NULL,
    join_date DATETIME NOT NULL
                       DEFAULT ( (DATETIME('now') ) ) 
);
```
2. Set the absolute path to the database in the `bot.py` file in the `BotDB` variable.
3. Create a `config.py` file and specify the bot's telegram token in the `BOT_TOKEN` variable
4. In the project directory use `poetry install` to install the required libraries.
5. To start the bot use from project root directory `poetry run python finance_manager/bot.py` or run with python `bot.py`