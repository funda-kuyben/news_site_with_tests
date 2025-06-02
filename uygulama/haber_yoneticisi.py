from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .veritabani import veritabani, Haber

# Blueprint tanımlanıyor
haber_bp = Blueprint("haber", __name__)

# Ana sayfa: HTML ile haberleri listeler
@haber_bp.route('/')
def ana_sayfa():
    haberler = Haber.query.all()
    return render_template("index.html", haberler=haberler)

# HTML Form ile haber ekleme
@haber_bp.route('/haber-ekle-form', methods=['GET', 'POST'])
def haber_ekle_form():
    if request.method == 'POST':
        baslik = request.form.get('baslik')
        icerik = request.form.get('icerik')
        if baslik and icerik:
            yeni = Haber(baslik=baslik, icerik=icerik)
            veritabani.session.add(yeni)
            veritabani.session.commit()
            return redirect(url_for('haber.ana_sayfa'))
    return render_template("ekle.html")

# API ile JSON üzerinden haber ekleme
@haber_bp.route('/haber-ekle', methods=['POST'])
def haber_ekle_api():
    veri = request.get_json()
    baslik = veri.get('baslik')
    icerik = veri.get('icerik')

    if not baslik or not icerik:
        return jsonify({'hata': 'Başlık ve içerik gerekli.'}), 400

    yeni_haber = Haber(baslik=baslik, icerik=icerik)
    veritabani.session.add(yeni_haber)
    veritabani.session.commit()
    return jsonify({'mesaj': 'Haber başarıyla eklendi.'}), 201

# API ile tüm haberleri JSON olarak getir
@haber_bp.route('/haberler', methods=['GET'])
def haberleri_getir():
    haberler = Haber.query.all()
    return jsonify([
        {
            'id': h.id,
            'baslik': h.baslik,
            'icerik': h.icerik,
            'tarih': h.yayin_tarihi.strftime('%Y-%m-%d %H:%M')
        } for h in haberler
    ])

# API ile haber silme
@haber_bp.route('/haber-sil/<int:id>', methods=['DELETE'])
def haber_sil(id):
    try:
        haber = Haber.query.get(id)
        if not haber:
            return jsonify({'hata': f'{id} ID\'li haber bulunamadı.'}), 404

        veritabani.session.delete(haber)
        veritabani.session.commit()
        return jsonify({'mesaj': f'{id} ID\'li haber başarıyla silindi.'}), 200

    except Exception as e:
        veritabani.session.rollback()
        return jsonify({'hata': 'Sunucu hatası oluştu.', 'detay': str(e)}), 500
