from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

from flask import Flask, render_template



load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')




# TİD kuralları dosyalarını yükleyelim
with open("tid_kurallari.txt", "r", encoding="utf-8") as f:
    tid_kurallari = f.read()

with open("turkcetotid_kurallari.txt", "r", encoding="utf-8") as f:
    turkcetotid_kurallari = f.read()


def tid_turkce_ceviri(tid_sentence: str) -> str:
    prompt = f"""
    Aşağıdaki metin Türk İşaret Dili (TİD) yapısına göre yazılmıştır.
Yapı: [ZAMAN] [YER] [ÖZNE] [NESNE] [FİİL]

Cümleyi doğal ve doğru bir Türkçeye çevir.

Açıklama ekleme. Sadece çeviri sonucunu yaz. Yalnızca ÇEVİRİyi çıktı olarak ver.

Lütfen çeviri yaparken kelimelerin yerini doğru dizmekten daha önemlisi, cümlenin anlamını doğru aktarmaktır.

Eğer kelimeler eksiksiz olsa bile anlam bozulmuşsa, bu çeviri hatalı sayılır.

Anlamın bozulmaması için çeviride özne-fiil-nesne ilişkisini doğru kur.

Aşağıdaki çeviri kurallarına göre TİD'den Türkçeye çeviri yapmanı istiyorum:

    {tid_kurallari}
    TİD: {tid_sentence}
    Türkçesi:
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def turkce_tid_ceviri(turkce_sentence: str) -> str:
    prompt = f"""
    Türkçe cümleyi Türk İşaret Dili (TİD) kelimeleri şeklinde, kısa ve sade yaz.

Açıklama ekleme. Sadece çeviri sonucunu yaz.

Sadece anahtar işaret kelimeleri yaz, açıklama, madde işaretleri ve detay verme.

Türk İşaret Dilinin yapısının da aşağıdaki şekilde olduğunu unutma.
Yapı: [ZAMAN] [YER] [ÖZNE] [NESNE] [FİİL]

TİD işaret dilinde birleşik kelimelerin olduğunu unutma. Çevirirken onları o şekilde çevir.

Çeviride anlamı doğru korumak için özellikle aşağıdaki öğelere dikkat et:

TİDe çeviriken olumsuz anlam için "değil", "yok" kelimelerini fiilden sonra yaz. 
ÖRNEĞİN:
Sen yarın biz gelme. --> Yarın sen biz gelmek değil.

Soru sormak için 'S-Par' ifadesinin cümlenin sonuna yazarsan artık o cümle değil soru olmuş olur.

PİJAMA → UYKU + KIYAFET
BUZDOLABI → BUZ + DOLAP
ÇOCUK BEZİ → ÇOCUK + BEZ
SAKSI → ÇİÇEK + FANUS
DEMİRYOLU → TREN + YOL
SAHİL → DENİZ + KENAR
ABİYE → KIZ + KIYAFET
TERMOMETRE → SICAKLIK + DERECE
CÜBBE → İMAM + KABAN
TABLO → FOTOĞRAF + ÇERÇEVE
PSİKOLOG → PSİKOLOJİ + DOKTOR
RÖTAR → SAAT + GEÇ
AYAZ → HIZLI + SOĞUK

Yukarıda türkçedeki kelimelerin tidde birleşik kelime karşılıklarıdır. Çeviriyi ona göre yap.
Örneğin:
"sen yarın bize gelirken pijamalarını unutma" cümlesini şu şekilde çevir:
Yarın sen biz gelmek uyku+kıyafet getirmek unutmak değil.

Lütfen çeviri yaparken kelimelerin yerini doğru dizmekten daha önemlisi, cümlenin anlamını doğru aktarmaktır.

Eğer kelimeler eksiksiz olsa bile anlam bozulmuşsa, bu çeviri hatalı sayılır.

Anlamın bozulmaması için çeviride özne-fiil-nesne ilişkisini doğru kur.

- Zaman bilgisini eksiksiz aktar
- Fiilin olumlu/olumsuz olup olmadığını doğru göster ("değil" ekle)
- Özne kim olduğunu açık belirt (ben, sen, biz...)

Türkçe konuşma dilinden TİD'e çeviri yaparken fiillerin -mek, -mak halleirni kullan.
Örneğin: Oku=okumak, Yaz=Yazmak 

Türkçedeki “-se”, “-sa”, “ise”, “-diğinde” gibi koşullu yapılar TİD’de birebir çevrilmez.

Bunun yerine cümle şu şekilde çevrilmelidir:

“Sen gidersen, selam söyle.” “Sen gitmek, selam söylemek”

Koşul ifadesi önce gelir, sonra sonuç ifadesi gelir. Cümlede “ise” kelimesi yazılmaz.

Şu örnekleri incele:

Türkçe: Eğer yağmur yağarsa, dışarı çıkma.
TİD: Yağmur yağmak dışarı çıkmak değil

Türkçe: Sen gidersen, bana haber ver.
TİD: Sen gitmek ben haber vermek
    {turkcetotid_kurallari}
    Türkçe: {turkce_sentence}
    TİD:
    """
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    direction = data.get('direction')  # 'tid-tr' veya 'tr-tid'
    text = data.get('text')

    if not text or direction not in ['tid-tr', 'tr-tid']:
        return jsonify({'error': 'Geçersiz istek'}), 400

    try:
        if direction == 'tid-tr':
            result = tid_turkce_ceviri(text)
        else:
            result = turkce_tid_ceviri(text)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)