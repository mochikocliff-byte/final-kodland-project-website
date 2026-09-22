from flask import Flask, render_template, request

app = Flask(__name__)

# FAQ Database (semua jawaban dalam Python)
faq_data = {
    'penyebab': {
        'keywords': ['penyebab', 'sebab', 'kenapa', 'apa penyebab'],
        'answer': '''🔥 Penyebab perubahan iklim:
- Pembakaran bahan bakar fosil (batu bara, minyak, gas)
- Penebangan hutan besar-besaran
- Limbah industri dan asap kendaraan
- Peternakan skala besar menghasilkan gas metana

Semua ini meningkatkan gas rumah kaca di atmosfer.'''
    },
    'dampak': {
        'keywords': ['dampak', 'akibat', 'efek', 'apa dampak'],
        'answer': '''⚠️ Dampak yang sudah terlihat:
- Suhu bumi terus naik
- Permukaan air laut meningkat
- Cuaca ekstrem lebih sering terjadi
- Es di kutub mencair
- Hewan kehilangan habitat
- Banjir dan kekeringan lebih parah'''
    },
    'solusi': {
        'keywords': ['solusi', 'cara', 'apa yang bisa', 'bagaimana', 'membantu', 'lakukan'],
        'answer': '''💡 Yang bisa kita lakukan:
- Hemat energi listrik di rumah
- Gunakan transportasi umum atau sepeda
- Kurangi sampah plastik
- Tanam dan rawat pohon
- Kurangi konsumsi daging
- Pilih produk ramah lingkungan

Setiap tindakan kecil membuat perbedaan.'''
    },
    'gas': {
        'keywords': ['gas rumah kaca', 'greenhouse', 'CO2', 'karbon', 'emisi'],
        'answer': '''💨 Gas rumah kaca:
Gas yang menjebak panas di atmosfer, terdiri dari:
- CO2 (karbon dioksida) - dari pembakaran bahan bakar
- CH4 (metana) - dari peternakan dan limbah
- N2O (nitrous oxide) - dari pupuk dan industri
- Gas fluorinated - dari pendingin

Semakin banyak gas, semakin panas bumi.'''
    },
    'suhu': {
        'keywords': ['suhu', 'temperatur', 'panas', 'naik', 'berapa', 'derajat'],
        'answer': '''🌡️ Fakta suhu bumi:
Suhu rata-rata bumi sudah naik sekitar 1.1°C sejak 150 tahun lalu.

Akibatnya:
- Gelombang panas lebih sering dan kuat
- Musim tidak terprediksi
- Hewan stres dengan perubahan suhu
- Tanaman terganggu jadwal pertumbuhannya'''
    },
    'laut': {
        'keywords': ['air laut', 'permukaan laut', 'laut naik', 'banjir', 'pulau'],
        'answer': '''🌊 Air laut naik karena:
- Es di kutub mencair, air mengalir ke laut
- Air laut memuai saat suhu naik

Bahayanya:
- Pulau kecil bisa tenggelam
- Kota pesisir terendam
- Ekosistem laut rusak
- Nelayan kehilangan mata pencaharian'''
    },
    'hutan': {
        'keywords': ['hutan', 'pohon', 'kayu', 'deforestasi', 'penebangan'],
        'answer': '''🌳 Hutan sangat penting:
- Menyerap CO2 dari udara
- Menghasilkan oksigen
- Rumah bagi jutaan spesies hewan
- Mengatur pola curah hujan

Saat hutan ditebang:
- CO2 meningkat
- Hewan kehilangan rumah
- Banjir dan erosi tanah meningkat'''
    },
    'peternakan': {
        'keywords': ['peternakan', 'daging', 'sapi', 'metana', 'pertanian'],
        'answer': '''🐄 Peternakan dan iklim:
- Sapi dan kambing menghasilkan gas metana
- Pupuk pakan menghasilkan emisi
- Deforestasi untuk lahan ternak
- Limbah mencemari air

Tips: kurangi porsi daging, coba hari tanpa daging, pilih ternak berkelanjutan.'''
    },
    'transportasi': {
        'keywords': ['transportasi', 'mobil', 'bensin', 'polusi', 'kendaraan'],
        'answer': '''🚗 Transportasi dan emisi:
- Pembakaran bensin menghasilkan CO2 besar
- Asap kendaraan berbahaya bagi kesehatan
- Polusi udara tinggi di kota

Solusi: gunakan transportasi publik, sepeda, carpool, atau kendaraan listrik.'''
    },
    'energi': {
        'keywords': ['energi', 'listrik', 'batu bara', 'bahan bakar fosil', 'pembangkit'],
        'answer': '''⚡ Energi penyumbang emisi terbesar:
- Pembangkit batu bara sangat berpolusi
- Rumah tangga dan industri butuh energi besar

Cara hemat: matikan lampu tidak dipakai, gunakan lampu LED, kurangi AC, gunakan panel surya.'''
    },
    'sampah': {
        'keywords': ['sampah', 'plastik', 'limbah', 'daur ulang'],
        'answer': '''♻️ Sampah plastik:
- Butuh ratusan tahun untuk terurai
- Mencemari laut dan membahayakan hewan
- Produksi plastik menghasilkan emisi besar

Solusi: gunakan tas kain, hindari plastik sekali pakai, daur ulang dengan benar.'''
    },
    'kutub': {
        'keywords': ['kutub', 'es', 'arktik', 'antartika'],
        'answer': '''🧊 Es kutub penting karena:
- Memantulkan panas matahari kembali ke luar angkasa
- Mengatur arus laut dan cuaca global
- Menjadi rumah bagi beruang kutub dan penguin

Saat es mencair, laut menyerap lebih banyak panas dan permukaan laut naik.'''
    },
    'cuaca': {
        'keywords': ['cuaca ekstrem', 'badai', 'angin', 'banjir', 'kekeringan', 'topan'],
        'answer': '''⛈️ Cuaca ekstrem meningkat:
- Badai dan topan lebih kuat
- Banjir lebih parah dan sering
- Kekeringan bertahan lebih lama
- Gelombang panas lebih mematikan

Persiapan: kenali jalur evakuasi, siapkan stok air dan makanan, pasang aplikasi peringatan bencana.'''
    },
    'spesies': {
        'keywords': ['spesies', 'hewan', 'punah', 'kepunahan', 'tumbuhan'],
        'answer': '''🦁 Spesies terancam punah karena:
- Habitat hilang
- Perubahan suhu drastis
- Laut menghangat
- Pencemaran lingkungan

Contoh hewan terancam: beruang kutub, penguin, terumbu karang, orangutan, gajah, paus.'''
    },
    'kesehatan': {
        'keywords': ['kesehatan', 'penyakit', 'udara', 'polusi'],
        'answer': '''😷 Dampak pada kesehatan:
- Polusi udara menyebabkan penyakit paru
- Panas ekstrem menyebabkan stroke panas
- Penyakit menular dari hewan meningkat
- Gagal panen menyebabkan malnutrisi

Menjaga lingkungan sama dengan menjaga kesehatan.'''
    },
    'teknologi': {
        'keywords': ['teknologi', 'panel surya', 'energi terbarukan', 'hijau'],
        'answer': '''🔬 Teknologi hijau:
- Panel surya menghasilkan listrik dari matahari
- Turbin angin menghasilkan energi bersih
- Mobil listrik tanpa emisi
- Teknologi penangkap karbon (carbon capture)

Investasi di teknologi hijau adalah investasi masa depan.'''
    },
    'generasi': {
        'keywords': ['generasi muda', 'anak', 'masa depan', 'gen z'],
        'answer': '''👨‍👧‍👦 Generasi muda dan iklim:
- Merekalah yang paling merasakan dampaknya di masa depan
- Punya peran besar dalam gerakan perubahan iklim
- Bisa membawa ide dan inovasi baru

Perubahan dimulai dari langkah kecil hari ini.'''
    }
}

def cari_jawaban(pertanyaan):
    """Cari jawaban berdasarkan keywords"""
    p = pertanyaan.lower()

    for key, data in faq_data.items():
        for keyword in data['keywords']:
            if keyword in p:
                return data['answer']

    # Jika tidak ada yang cocok
    return '''🤔 Saya belum punya jawaban untuk itu.

Coba tanya tentang:
- Penyebab perubahan iklim
- Dampak yang terjadi
- Solusi dan cara membantu
- Energi dan transportasi
- Sampah dan plastik
- Kesehatan dan iklim
- Teknologi hijau
- Generasi muda'''

@app.route("/", methods=["GET", "POST"])
def index():
    jawaban = ""

    if request.method == "POST":
        pertanyaan = request.form.get("pertanyaan", "").strip()

        if pertanyaan:
            jawaban = cari_jawaban(pertanyaan)

    return render_template("index.html", jawaban=jawaban)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
