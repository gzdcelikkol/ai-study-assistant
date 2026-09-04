# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam, ChatCompletion
from schemas.quiz import GenerateQuizRequest, EvaluateAnswerRequest
from core.config import llm_model_name, groq_api_key
from schemas.question import QuestionRequest
from services.pdf_service import process_pdf
from services.embedding_service import get_embeddings_batch, get_embedding
from services.vector_db import save_chunks_to_db, search_relevant_chunks
import json
from schemas.flashcard import GenerateFlashcardsRequest, FlashcardsResponse, FlashcardItem
from services.memory_service import get_chat_history, add_message_to_history
app = FastAPI(title="AI Student Assistant")
groq_client = Groq(api_key=groq_api_key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# main.py içine eklenecek seviye profilleri
LEVEL_INSTRUCTIONS = {
    "eli5": (
        "Hedef Kitle: 5 yaşında bir çocuk (Feynman Tekniği). "
        "Teknik jargondan, karmaşık matematiksel terimlerden tamamen kaçın. "
        "Kavramları oyuncaklar, mutfak, oyun parkı veya gündelik basit analojilerle anlat. "
        "Çok samimi, sade ve eğlenceli bir ton kullan."
    ),
    "beginner": (
        "Hedef Kitle: Yazılıma yeni başlayan 1. sınıf öğrencisi. "
        "Temel kavramları net açıkla, terimleri ilk kez duyuyormuş gibi tanımla, "
        "basit kod örnekleri veya net görsel metaforlar ver."
    ),
    "intermediate": (
        "Hedef Kitle: Lisans düzeyinde bilgisayar mühendisliği öğrencisi. "
        "Standart teknik terminolojiyi, Big O analizini ve temel algoritmik avantaj/dezavantajları kullan."
    ),
    "academic": (
        "Hedef Kitle: Akademik araştırmacı / İleri düzey mühendis. "
        "Resmi, analitik ve derinlemesine bir üslup kullan. "
        "Bellek yerleşimi, önbellek verimliliği, asimptotik sınırlar ve mimari detaylara odaklan."
    )
}

@app.get("/")
def home():
    return {"message": "Hello Study Assistant"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyaları desteklenir.")

    file_bytes = await file.read()
    page_count, chunks = process_pdf(file_bytes)

    # Embedding çıkarma ve DB'ye kaydetme
    embeddings = get_embeddings_batch(chunks)
    save_chunks_to_db(file.filename, chunks, embeddings)

    return {
        "file_name": file.filename,
        "page_count": page_count,
        "saved_chunks": len(chunks)
    }

@app.post("/question")
def ask_question(request: QuestionRequest):
    try:
        session_id = request.session_id
        question_vector = get_embedding(request.question) # sorunun embeddingi
        relevant_chunks = search_relevant_chunks(question_vector, top_k=10) # chromaDB'den soruyla en ilgli 10 metin parçasını bulur
        context = "\n---\n".join(relevant_chunks)

        level_instruction = LEVEL_INSTRUCTIONS.get(request.level, LEVEL_INSTRUCTIONS["intermediate"])

        if request.mode == "socratic":
            system_message = (
                f"Zorluk Seviyesi: {level_instruction}\n"
                "You are a patient and wise university teaching assistant who uses the Socratic method to teach."
                "YOUR TASK: NEVER give a direct, prepared answer to a student’s question!"
                "Use the context of the lecture notes provided below to guide the student step by step."
                "Give a brief hint to help them find the answer, and then ask them a single thought-provoking, guiding counter-question."
                "If the student gets close to the correct answer, congratulate them and ask what the next logical step is."
            )
        else:
            system_message = (
                f"Zorluk Seviyesi: {level_instruction}\n"
                "You are a university teaching assistant. The relevant sections from the lecture notes are provided below."
                "Answer the student's question based on the information in these lecture notes."
                "If the answer is not explicitly stated in the lecture notes, explain it using your general knowledge, but note that it is not included in the notes."
            )

        # mesaj listesi
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_message},
        ]
        # varsa sohbet geçmişini de ekle
        past = get_chat_history(session_id)
        messages.extend(past)

        # yeni soru ve pdf
        new_user_m = f"Ders Notu İçeriği:\n{context}\n\nÖğrencinin Sorusu:\n{request.question}"
        messages.append({"role": "user", "content": new_user_m})

       # LLM çağrısı
        chat_completion: ChatCompletion = groq_client.chat.completions.create(
            messages=messages,
            model=llm_model_name )


        ai_answer = chat_completion.choices[0].message.content
        add_message_to_history(session_id, role="user", content=request.question)
        add_message_to_history(session_id, role="assistant", content=ai_answer)

        return {
            "session_id": session_id,
            "mode" : request.mode,
            "level" : request.level,
            "question": request.question,
            "answer": chat_completion.choices[0].message.content,
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/quiz/generate")
def generate_quiz(request: GenerateQuizRequest):
    try:
        # Konuyla ilgili ders notu parçalarını çekiyoruz
        topic_vector = get_embedding(request.topic)
        context_chunks = search_relevant_chunks(topic_vector, top_k=3)
        context = "\n---\n".join(context_chunks)

        prompt = f"""Aşağıdaki ders notlarını kullanarak öğrencinin bilgisini sınayacak 1 adet açık uçlu sınav sorusu hazırla.
Sorunun cevabı notlarda açıkça bulunabilir olsun. Sadece soruyu yaz.

Ders Notları:
{context}

Konu: {request.topic}
"""
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen adil ve net sorular soran bir sınav hazırlayıcısısın."},
                {"role": "user", "content": prompt}
            ],
            model=llm_model_name
        )
        return {"topic": request.topic, "generated_question": response.choices[0].message.content}
    except Exception as e:
        return {"hata": str(e)}

@app.post("/quiz/evaluate")
def evaluate_answer(request: EvaluateAnswerRequest):
    try:
        query_vector = get_embedding(request.question)
        context_chunks = search_relevant_chunks(query_vector, top_k=3)
        context = "\n---\n".join(context_chunks)

        prompt = f"""Sen bir ders hocasısın. Aşağıdaki ders notlarına dayanarak öğrencinin sınav cevabını değerlendir.

Ders Notları (Referans):
{context}

Soru: {request.question}
Öğrencinin Cevabı: {request.user_answer}

Lütfen şu formatta yanıt ver:
- Puan: 100 üzerinden bir not (Örn: 85/100)
- Doğru Noktalar: Öğrencinin doğru bildiği kısımlar
- Eksikler / Yanlışlar: Eksik bıraktığı veya yanlış açıkladığı yerler
- İdeal Cevap Özeti: Notlara göre olması gereken ideal cevap
"""
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen adil, yapıcı geri bildirim veren bir akademisyensin."},
                {"role": "user", "content": prompt}
            ],
            model=llm_model_name
        )
        return {
            "question": request.question,
            "user_answer": request.user_answer,
            "feedback": response.choices[0].message.content
        }
    except Exception as e:
        return {"hata": str(e)}

@app.post("/flashcards/generate", response_model=FlashcardsResponse)
def generate_flashcards(request: GenerateFlashcardsRequest):
    try:
        #Konuyla ilgili contexti buluruz
        topic_vector = get_embedding(request.topic)
        context_chunks = search_relevant_chunks(topic_vector, top_k=4)
        context = "\n---\n".join(context_chunks)

        # 2. JSON formatında çıktı vermesi için katı prompt hazırla
        prompt = f"""Aşağıdaki ders notlarını kullanarak aralıklı tekrar (spaced repetition) için {request.card_count} adet flashcard üret.
Her kartın ön yüzü (front) açık bir soru/terim, arka yüzü (back) ise kısa ve net açıklaması olmalıdır.

YANITI SADECE GEÇERLİ BİR JSON DİZİSİ OLARAK DÖN. Hiçbir açıklama metni ekleme.
Örnek format:
[
  {{"front": "LIFO nedir?", "back": "Last In, First Out; son giren elemanın ilk çıkması prensibidir."}}
]

Ders Notları:
{context}

Konu: {request.topic}
"""

        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen yalnızca JSON üreten bir eğitim materyali hazırlayıcısısın."},
                {"role": "user", "content": prompt}
            ],
            model=llm_model_name
        )

        raw_content = response.choices[0].message.content.strip()

        # Markdown kod bloğu (```json ... ```) temizliği
        if raw_content.startswith("```"):
            raw_content = raw_content.split("```")[1]
            if raw_content.startswith("json"):
                raw_content = raw_content[4:]
        raw_content = raw_content.strip()

        cards_data = json.loads(raw_content)

        flashcards_list = [FlashcardItem(front=card["front"], back=card["back"]) for card in cards_data]

        # 3. Anki uyumlu CSV/TSV formatı
        anki_lines = [f'"{card.front}";"{card.back}"' for card in flashcards_list]
        anki_csv = "\n".join(anki_lines)

        return FlashcardsResponse(
            topic=request.topic,
            total_cards=len(flashcards_list),
            flashcards=flashcards_list,
            anki_csv_format=anki_csv
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kart üretilirken hata oluştu: {str(e)}")


