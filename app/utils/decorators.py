# login_required 裝飾器
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(fun):  # 接收一個函式
    @wraps(fun)  # 保留原函式資訊
    def wrapper(*args, **kwargs):  # 建立一個新的包裝函式 # 接收原函式所以有參數
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))  # 如果用戶未登入
        return fun(*args, **kwargs)  # 呼叫原本的函式，並把參數原封不動傳進去 # 如果用戶已登入
    return wrapper  # 回傳包裝好的函式
