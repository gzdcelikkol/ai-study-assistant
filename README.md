# 🎓 AI Study Assistant (Yapay Zeka Destekli Ders Asistanı)

**AI Study Assistant**, ders notlarınızı (PDF) yükleyip içeriğiyle doğrudan etkileşime geçmenizi sağlayan **RAG (Retrieval-Augmented Generation)** tabanlı akıllı bir çalışma ortamıdır. 

Sadece düz cevaplar vermekle kalmaz; **Sokratik yöntemle** sizi yönlendirir, bilginizi **Feynman Tekniği (ELI5)** dahil 4 farklı seviyede test eder, **açık uçlu sınavlar hazırlayıp cevaplarınızı puanlar** ve **Anki uyumlu hafıza kartları (Flashcards)** üretir.

---

## 🌟 Öne Çıkan Özellikler

- 📄 **PDF Yükleme & Otomatik Parçalama (Chunking):** Ders notlarınız sayfalarına ayrılır ve işlenebilir parçalara bölünür.
- 🧠 **Semantik Arama (ChromaDB + Sentence-Transformers):** Notlarınız matematiksel vektörlere (`all-MiniLM-L6-v2`) dönüştürülür. Bir soru sorduğunuzda sadece anahtar kelimeler değil, **anlamca en yakın** ders notu kısımları bulunup modele verilir.
- 💡 **Öğrenme Modları:**
  - **Standart Mod:** Ders notlarındaki bilgilere sadık kalarak sorunuzu doğrudan ve net bir şekilde açıklar.
  - **Sokratik Mod:** Asla hazır cevap vermez! İpuçları ve karşı sorularla cevabı sizin bulmanızı sağlar.
- 🎯 **Anlatım & Zorluk Seviyeleri:**
  - `ELI5` *(Explain Like I'm 5)*: Feynman tekniğiyle, gündelik basit analojilerle anlatır.
  - `Beginner`: Yazılıma/konuya yeni başlayan öğrenci diliyle anlatır.
  - `Intermediate`: Üniversite lisans düzeyinde teknik terimlerle açıklar.
  - `Academic`: İleri düzey mühendislik ve akademik derinlikte analiz sunar.
- 📝 **Otomatik Quiz & Yapıcı Değerlendirme:** Notlarınızdan 1 adet açık uçlu sınav sorusu üretir. Verdiğiniz cevabı 100 üzerinden puanlayıp doğru noktaları, eksikleri ve ideal cevabı raporlar.
- 🗂️ **Flashcard & Anki Desteği:** Notlardan soru-cevap kartları çıkarır. İster arayüzde kartları çevirerek çalışabilir, isterseniz popüler aralıklı tekrar uygulaması **Anki**'ye aktarabilirsiniz.
- 💬 **Sohbet Hafızası (Memory):** Oturum boyunca sorduğunuz önceki soruları ve asistanın yanıtlarını hatırlar.
- 🖥️ **Modern Kullanıcı Arayüzü:** Tarayıcı üzerinden kolayca kullanılabilen temiz ve responsive web paneli.

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

Bu projenin çalışması için kullanılan temel kütüphaneler ve görevleri:

| Kütüphane | Ne İşe Yarar? |
| :--- | :--- |
| **FastAPI** | Yüksek performanslı, modern Python web ve API çatısı. |
| **Uvicorn** | FastAPI uygulamasını çalıştıran ASGI web sunucusu. |
| **Groq (`groq`)** | Llama / GPT açık kaynaklı LLM modellerini ultra hızlı çalıştıran yapay zeka servisi. |
| **Sentence-Transformers** | Metinleri anlamsal vektörlere dönüştüren açık kaynaklı yapay zeka kütüphanesi (`all-MiniLM-L6-v2`). |
| **ChromaDB (`chromadb`)** | Vektörleri ve ders notlarını yerel diskte saklayıp arayan vektör veritabanı. |
| **PyPDF (`pypdf`)** | Yüklenen PDF belgelerinin metinlerini okuyup ayrıştıran kütüphane. |
| **Pydantic** | Veri modelleri, doğrulama ve tip denetimi. |
| **python-dotenv** | `.env` dosyasındaki gizli API anahtarlarını güvenle projeye yükler. |
| **python-multipart** | Tarayıcıdan dosya (PDF) yükleme işlemlerini işler. |

---

## 🚀 Sıfırdan Adım Adım Kurulum (Başlangıç Rehberi)

Hiçbir ön bilginiz olmadan projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın:

### 1. Python Kurulumu
Bilgisayarınızda Python 3.10 veya daha yeni bir sürümün yüklü olduğundan emin olun.
- [python.org/downloads](https://www.python.org/downloads/) adresinden indirebilirsiniz.
- ⚠️ **Önemli (Windows):** Kurulum yaparken en alttaki **"Add Python to PATH"** kutucuğunu mutlaka işaretleyin!

### 2. Projeyi Bilgisayarınıza İndirin
Terminali veya komut istemcisini (PowerShell / CMD) açın:
```bash
git clone https://github.com/gzdcelikkol/ai-study-assistant.git
cd ai-study-assistant
```

### 3. Sanal Ortam (Virtual Environment) Oluşturun
Projeye ait paketlerin sisteminizdeki diğer projelere karışmaması için izole bir ortam oluşturuyoruz:

- **Windows (PowerShell / CMD):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
  *(Not: PowerShell'de yetkilendirme hatası alırsanız `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` komutunu çalıştırabilirsiniz).*

- **Mac / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
Ortam aktifleştiğinde komut satırınızın başında `(venv)` ibaresini görürsünüz.

### 4. Gerekli Kütüphaneleri Yükleyin
Tek bir komutla tüm bağımlılıkları indirin:
```bash
pip install -r requirements.txt
```
*(Bu işlem sentence-transformers ve PyTorch kütüphanelerini ilk kez indirirken birkaç dakika sürebilir).*

### 5. Groq API Anahtarını Ayarlayın
Yapay zeka yanıtlarının üretilmesi için ücretsiz bir Groq API anahtarına ihtiyacınız vardır:
1. [console.groq.com/keys](https://console.groq.com/keys) adresine gidin ve ücretsiz bir hesap açıp **Create API Key** butonuna tıklayın.
2. Proje ana dizininde bulunan `.env.example` dosyasını kopyalayarak `.env` adında yeni bir dosya oluşturun:
   ```powershell
   # Windows için
   copy .env.example .env
   ```
3. `.env` dosyasını açıp anahtarınızı yapıştırın:
   ```env
   GROQ_API_KEY=gsk_sizin_aldiginiz_api_anahtari
   ```

---

## 🏃‍♂️ Uygulamayı Çalıştırma

### 1. Backend API Sunucusunu Başlatın
Terminalinizde (sanal ortam aktifken) şu komutu çalıştırın:
```bash
uvicorn main:app --reload
```
Sunucu başarıyla başladığında şu çıktıyı göreceksiniz:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 2. Kullanıcı Arayüzünü Açın
- `frontend/index.html` dosyasına çift tıklayarak herhangi bir web tarayıcısında (Chrome, Edge, Firefox vb.) açın.
- Artık sol panelden PDF yükleyebilir, mod/seviye seçebilir, sağdaki chat ekranından sorular sorabilir veya Quiz/Flashcard oluşturabilirsiniz!

---

## 📂 Proje Klasör Yapısı

```text
ai-study-assistant/
│
├── core/
│   ├── config.py                 # Ortam değişkenleri ve model ayarları
│   └── __init__.py
│
├── frontend/
│   └── index.html                # Modern Web arayüzü (Tailwind CSS tabanlı)
│
├── schemas/                      # İstek ve yanıt Pydantic şablonları
│   ├── flashcard.py              # Flashcard modelleri
│   ├── question.py               # Soru-cevap modelleri & zorluk seviyeleri
│   └── quiz.py                   # Quiz üretme ve değerlendirme modelleri
│
├── services/                     # İş mantığı ve servisler
│   ├── embedding_service.py      # Metin vektörleştirme (Sentence-Transformers)
│   ├── memory_service.py         # Sohbet geçmişi (Session memory)
│   ├── pdf_service.py            # PDF okuma ve metin parçalama (Chunking)
│   └── vector_db.py              # ChromaDB vektör veritabanı işlemleri
│
├── .env.example                  # Ortam değişkeni şablonu
├── .gitignore                    # Git tarafından takip edilmeyecek dosyalar
├── main.py                       # FastAPI ana uygulama ve endpoint'ler
├── README.md                     # Proje dokümantasyonu
└── requirements.txt              # Proje bağımlılıkları listesi
```

---

## 📡 API Uç Noktaları (Endpoints)

FastAPI otomatik Swagger dokümantasyonu sunar. Sunucu çalışırken [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresini ziyaret ederek tüm endpoint'leri canlı olarak test edebilirsiniz:

| Metot | Uç Nokta | Açıklama |
| :--- | :--- | :--- |
| `GET` | `/` | Asistan karşılama ve sağlık kontrolü. |
| `POST` | `/upload-pdf` | PDF yükler, metin parçalarını vektörleştirip ChromaDB'ye kaydeder. |
| `POST` | `/question` | İlgili not parçalarını bularak Sokratik veya Standart modda yanıt üretir. |
| `POST` | `/quiz/generate` | Notlardan açık uçlu 1 sınav sorusu hazırlar. |
| `POST` | `/quiz/evaluate` | Öğrencinin sınav cevabını değerlendirir ve 100 üzerinden not verir. |
| `POST` | `/flashcards/generate` | Aralıklı tekrar için soru-cevap kartları ve Anki CSV formatı üretir. |

---

## ❓ Sık Karşılaşılan Sorunlar ve Çözümleri

1. **`ModuleNotFoundError: No module named '...'`**
   - **Çözüm:** Sanal ortamınızın aktif olduğundan emin olun (`(venv)` görünmeli). Ardından `pip install -r requirements.txt` komutunu tekrar çalıştırın.
2. **`Groq API Key Bulunamadı` Hatası**
   - **Çözüm:** Ana dizinde `.env` dosyasının adının doğru olduğundan (Windows bazen `.env.txt` yapabilir) ve içinde `GROQ_API_KEY=...` satırının bulunduğundan emin olun.
3. **PowerShell Komut Çalıştırma Hatası (`running scripts is disabled`)**
   - **Çözüm:** PowerShell'i açıp şu komutu verin:
     ```powershell
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     ```
4. **CORS Hatası**
   - **Çözüm:** Projede `CORSMiddleware` tüm originlere (`*`) açık olarak ayarlanmıştır. `main.py` sunucusunun arka planda `http://127.0.0.1:8000` portunda çalıştığından emin olun.

---

