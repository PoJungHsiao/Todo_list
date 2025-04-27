# 專案入口，可以執行 Flask 應用
from app import create_app

app = create_app()

# 確保這段程式只在直接執行該檔案時才會執行，不會在被其他模組匯入時執行 app.run()。
if __name__ == '__main__':
    app.run(debug=True)
