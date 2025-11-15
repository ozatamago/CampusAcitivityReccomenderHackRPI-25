# app/__init__.py
import os
from flask import Flask, jsonify

from .extensions import db, migrate

def create_app(config_object=None):
    """
    Flask アプリケーションファクトリ。
    config_object を渡せばそれを使い、無ければ DevConfig を使う。
    """
    app = Flask(__name__, instance_relative_config=True)

    # ------- 設定ロード -------
    if config_object is not None:
        app.config.from_object(config_object)
    else:
        # デフォルトは DevConfig を使用
        from config import DevConfig
        app.config.from_object(DevConfig)

    # instance フォルダを確実に作っておく（SQLite 用）
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # ------- 拡張の初期化 -------
    db.init_app(app)
    migrate.init_app(app, db)

    # ------- Blueprint の登録 -------
    # main
    from .main.routes import main_bp
    app.register_blueprint(main_bp)

    # api
    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # calendar
    from .calendar.routes import calendar_bp
    app.register_blueprint(calendar_bp, url_prefix="/calendar")

    # auth（必要なら）
    try:
        from .auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/auth")
    except ImportError:
        # auth をまだ作ってない場合でも落ちないようにする
        pass

    # ------- ヘルスチェック用ルート -------
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "CampusMatching backend"})

    return app
