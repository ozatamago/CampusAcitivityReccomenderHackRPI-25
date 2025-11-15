# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # デバッグ用
    app.run(debug=True)
