import unittest
from uygulama import uygulamayi_olustur, veritabani
from uygulama.veritabani import Haber

class HaberTesti(unittest.TestCase):
    def setUp(self):
        self.uygulama = uygulamayi_olustur({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })

        self.app_context = self.uygulama.app_context()
        self.app_context.push()
        veritabani.create_all()
        self.istemci = self.uygulama.test_client()

    def tearDown(self):
        veritabani.session.remove()
        veritabani.drop_all()
        self.app_context.pop()

    def test_haber_ekleme(self):
        yanit = self.istemci.post('/haber-ekle', json={
            'baslik': 'Test Başlık',
            'icerik': 'Bu bir test içeriğidir.'
        })
        self.assertEqual(yanit.status_code, 201)
        self.assertEqual(yanit.get_json().get('mesaj'), 'Haber başarıyla eklendi.')

    def test_haber_listeleme(self):
        self.istemci.post('/haber-ekle', json={
            'baslik': 'Başlık',
            'icerik': 'İçerik'
        })
        yanit = self.istemci.get('/haberler')
        veriler = yanit.get_json()
        self.assertEqual(len(veriler), 1)
        self.assertEqual(veriler[0]['baslik'], 'Başlık')
