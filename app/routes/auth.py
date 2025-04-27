# 註冊、登入/登出 功能的 routes
# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
from config import db_config, db_name
import bcrypt  # 加密套件

# 模組化 # 定義一個 Blueprint 物件，用來組織整個 auth.py 裡的所有路由（routes）
auth_bp = Blueprint('auth', __name__)

# 註冊功能建立


@auth_bp.route('/register', methods=['GET', 'POST'])  # 裝飾器 # 定義URL與接受請求方式
def register():
    if request.method == "POST":
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].encode('utf-8')  # bcrypt 要 bytes

        # 密碼加密
        hash_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            # 連線到資料庫
            with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
                # 檢查是否有相同帳號或email
                cursor.execute(
                    "SELECT id FROM USER WHERE email = %s OR username = %s", (email, username))
                result = cursor.fetchone()
                if result:
                    flash('使用者名稱或信箱已存在')  # 使用者提示訊息
                    # 根據函式名稱反查對應URL # 頁面重新導向註冊頁面
                    return redirect(url_for('auth.register'))
                else:
                    sql = "INSERT INTO USER (username, email, password, is_active) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (username, email, hash_pw, True))
                    conn.commit()  # 資料庫變更提交
                    flash('✅ 註冊成功，請登入')  # 使用者提示訊息
                    return redirect(url_for('auth.login'))  # 導向登入畫面
        except Exception as e:
            print(f"[錯誤] 註冊失敗: {e}")  # 開發端顯示錯誤訊息
            flash('註冊失敗，請稍後再試')  # 使用者提示訊息
            return redirect(url_for('auth.register'))  # 重新導向註冊畫面

    return render_template('register.html')  # 使用者是用 GET 方法（只是開啟註冊頁面）這裡才會被執行

# 登入功能鍵立


@auth_bp.route('/login', methods=['GET', 'POST'])  # 裝飾器 # 定義URL與接受請求方式
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].encode('utf-8')

        try:
            # 連線到資料庫並查詢帳號是否存在
            with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM USER WHERE username = %s", (username,))
                user = cursor.fetchone()

                # 判斷是否查到帳號並依結果進入不同決策
                if user:
                    check_pw = bcrypt.checkpw(
                        password, user['password'])  # 如果帳號存在比對密碼
                    if check_pw:
                        # 把使用者資訊存進 Flask 的 session，讓接下來的頁面可以識別「誰登入了」
                        session['user_id'] = user['id']
                        session['username'] = username
                        flash('✅ 登入成功')  # 使用者提示訊息
                        # 登入成功進入使用者Todo系統畫面
                        return redirect(url_for('todo.dashboard'))
                    else:
                        flash('❌ 密碼錯誤')  # 使用者提示訊息
                        return redirect(url_for('auth.login'))  # 重新導向登入畫面
                else:
                    flash('此帳號尚未註冊，請註冊後再登入')
                    return redirect(url_for('auth.register'))  # 重新導向註冊畫面
        except Exception as e:
            print(f"[錯誤] 登入失敗: {e}")  # 開發端顯示錯誤訊息
            flash('登入失敗，請稍後再試')  # 使用者提示訊息
            return redirect(url_for('auth.login'))  # 重新導向登入畫面

    return render_template('login.html')  # 使用者是用 GET 方法（只是開啟登入頁面）這裡才會被執行

# 登出功能建立


@auth_bp.route('/logout', methods=['GET'])  # 裝飾器 # 定義URL與接受請求方式
def logout():
    session.clear()  # 清除所有登入時存入的 session 資料
    flash('👋 已成功登出')  # 使用者提示訊息
    return redirect(url_for('auth.login'))  # 重新導向登入頁面
