from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)


@main_bp.route('/')  # 首頁路由
def home():
    if 'username' not in session:  # 如果使用者未登入，重定向到登入畫面
        return redirect(url_for('auth.login'))
    else:
        # 已登入，重新定向到任務清單頁面
        return redirect(url_for('todo.dashboard'))
