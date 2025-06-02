from flask import Flask
from .veritabani import veritabani
from .haber_yoneticisi import haber_bp

def uygulamayi_olustur(test_config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haberler.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    veritabani.init_app(app)

    # Uygulama bağlamında tablo oluştur (yalnızca tablo yoksa)
    with app.app_context():
        veritabani.create_all()

    app.register_blueprint(haber_bp)

    return app
