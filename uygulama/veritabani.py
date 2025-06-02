from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

veritabani = SQLAlchemy()

class Haber(veritabani.Model):
    __tablename__ = 'haberler'
    __table_args__ = {'extend_existing': True}

    id = veritabani.Column(veritabani.Integer, primary_key=True)
    baslik = veritabani.Column(veritabani.String(200), nullable=False)
    icerik = veritabani.Column(veritabani.Text, nullable=False)
    yayin_tarihi = veritabani.Column(veritabani.DateTime, default=lambda: datetime.now(UTC))
