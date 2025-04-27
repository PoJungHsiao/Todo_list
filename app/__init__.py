# 建立 Flask 應用、載入設定檔
from flask import Flask
from config import Config
from app.routes.auth import auth_bp
from app.routes.todo import todo_bp
from app.routes.main import main_bp


def create_app():
    app = Flask(__name__)  # 初始化 Flask 應用程式
    app.config.from_object(Config)  # 載入設定(從 config.py 裡 class Config)

    # 註冊路由模組
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(main_bp)
    return app
