# Todolist routes建立
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
from config import db_config, db_name
from app.utils.decorators import login_required

# 模組化 # 定義一個 Blueprint 物件，用來組織整個 todo.py 裡的所有路由（routes）
todo_bp = Blueprint('todo', __name__)

# 顯示任務清單


@todo_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        user_id = session['user_id']
        with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM TODO WHERE user_id = %s", (user_id,))
            todos = cursor.fetchall()
        return render_template('dashboard.html', task_list=todos)
    except Exception as e:
        print(f"[錯誤] 無法取得任務清單: {e}")  # 開發端顯示錯誤訊息
        flash("載入任務失敗")  # 使用者提示訊息
        return render_template('dashboard.html', task_list=[])

# 新增任務功能建立


@todo_bp.route('/add', methods=['POST'])
@login_required
def add_todo():
    # 嘗試取得表單欄位名稱為 'title' 的值，如果沒有這個欄位，就預設給一個空字串 ''（避免出錯）。
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    user_id = session['user_id']

    if not title:
        flash('請填寫任務標題')
        return redirect(url_for('todo.dashboard'))  # 重新導向任務清單

    try:
        # 連線到資料庫新增資料
        with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
            sql = '''INSERT INTO TODO (title, description, user_id) VALUES (%s, %s, %s)'''
            cursor.execute(sql, (title, description, user_id))
            conn.commit()  # 提交變更
            flash('✅ 任務新增成功')  # 使用者提示訊息
    except Exception as e:
        print(f"[錯誤] 新增任務失敗: {e}")  # 開發端顯示錯誤訊息
        flash('❌ 任務新增失敗，請稍後再試')  # 使用者提示訊息

    return redirect(url_for('todo.dashboard'))  # 重新導向任務清單

# 切換任務狀態功能建立


@todo_bp.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def toggle_complete(task_id):
    user_id = session['user_id']  # 確認目前登入者身分

    try:
        # 連線到資料庫
        with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
            # 查出任務是否屬於這個使用者，並抓取目前 completed 狀態
            cursor.execute(
                "SELECT completed FROM TODO WHERE id = %s AND user_id = %s", (
                    task_id, user_id)
            )
            task = cursor.fetchone()

            if not task:
                flash('❌ 查無此任務或無權限修改')  # 使用者提示訊息
                return redirect(url_for('todo.dashboard'))  # 重新導向任務清單

            # 反轉 completed 狀態
            new_status = not task['completed']
            cursor.execute(
                # 更新任務狀態
                "UPDATE TODO SET completed = %s WHERE id = %s AND user_id = %s", (
                    new_status, task_id, user_id)
            )
            conn.commit()  # 提交變更
            flash('✅ 任務狀態已更新')  # 使用者提示訊息
    except Exception as e:
        print(f"[錯誤] 更新任務狀態失敗: {e}")  # 開發端顯示錯誤訊息
        flash('❌ 更新任務狀態失敗，請稍後再試')  # 使用者提示訊息

    return redirect(url_for('todo.dashboard'))  # 重新導向任務清單

# 刪除任務功能建立


@todo_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_todo(task_id):
    user_id = session['user_id']

    try:
        # 連線到資料庫
        with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
            cursor.execute(
                # 刪除任務
                "DELETE FROM TODO WHERE id = %s AND user_id = %s", (task_id, user_id))
            conn.commit()  # 提交變更
            flash('🗑️ 任務已刪除')  # 使用者提示訊息
    except Exception as e:
        print(f"[錯誤] 刪除任務失敗: {e}")  # 開發端顯示錯誤訊息
        flash('❌ 任務刪除失敗，請稍後再試')  # 使用者提示訊息

    return redirect(url_for('todo.dashboard'))  # 重新導向任務清單

# 編輯任務功能建立


@todo_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(task_id):
    user_id = session['user_id']

    if request.method == 'POST':  # POST 請求進入 if
        # 提交表單，進行更新
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            flash('請填寫任務標題')
            # 導向編輯頁
            # 左邊的 task_id 為 url_for() 函式裡參數名稱（對應到 <int:task_id>），右邊的 task_id 為函式裡的變數
            return redirect(url_for('todo.edit_todo', task_id=task_id))

        try:
            # 連線到資料庫
            with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
                cursor.execute(
                    # 更新資料
                    "UPDATE TODO SET title = %s, description = %s WHERE id = %s AND user_id = %s",
                    (title, description, task_id, user_id)
                )
                conn.commit()  # 提交變更
                flash('✅ 任務更新成功')  # 使用者提示訊息
        except Exception as e:
            print(f"[錯誤] 任務更新失敗: {e}")  # 開發端顯示錯誤訊息
            flash('❌ 任務更新失敗，請稍後再試')  # 使用者提示訊息
        return redirect(url_for('todo.dashboard'))  # 重新導向任務清單

    else:
        # GET 請求進入編輯頁，顯示編輯畫面
        try:
            # 連線資料庫
            with pymysql.connect(database=db_name, **db_config) as conn, conn.cursor() as cursor:
                # 以任務 id 與 使用者 id 查找任務
                cursor.execute(
                    "SELECT * FROM TODO WHERE id = %s AND user_id = %s", (task_id, user_id))
                task = cursor.fetchone()

                if not task:  # 沒找到任務進入 if
                    flash('❌ 查無此任務或無權限編輯')  # 使用者提示訊息
                    return redirect(url_for('todo.dashboard'))  # # 重新導向任務清單
            # GET 請求進入編輯頁，顯示編輯畫面
            return render_template('edit.html', task=task)
        except Exception as e:
            print(f"[錯誤] 載入編輯畫面失敗: {e}")  # 開發端顯示錯誤訊息
            flash('❌ 載入編輯畫面失敗')  # 使用者提示訊息
            return redirect(url_for('todo.dashboard'))  # 重新導向任務清單
