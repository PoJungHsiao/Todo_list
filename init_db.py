# 建立資料庫(初始化)
import pymysql
from config import db_config, db_name

# 連線到伺服器並開啟指令游標
with pymysql.connect(**db_config) as conn, conn.cursor() as cursor:
    # 建立資料庫
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8mb4"
    )
    conn.commit()
    print("✅ 資料庫建立成功(或已存在)")

# 連線到剛建立的資料庫
with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
    # 建立使用者資料表
    sql = '''CREATE TABLE IF NOT EXISTS USER (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password BLOB NOT NULL,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE)'''
    cursor.execute(sql)
    conn.commit()
    print("✅ 使用者資料表建立成功(或已存在)")

# 連線到剛建立的資料庫
with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
    # 建立Todo資料表
    sql = '''CREATE TABLE IF NOT EXISTS TODO (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150),
    description VARCHAR(255),
    completed BOOLEAN DEFAULT FALSE,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES USER(id))'''
    cursor.execute(sql)
    conn.commit()
    print("✅ 代辦資料表建立成功(或已存在)")
