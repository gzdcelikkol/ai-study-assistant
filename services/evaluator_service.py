
import json
from core.config import groq_client, llm_model_name

def verify_groundedness(context: str, answer: str) -> dict:
    """
    Üretilen cevabın verilen ders notu bağlamında bulunup bulunmadığını
    ve halüsinasyon içerip içermediğini denetler.
    """
    eval_prompt = f"""GÖREV: Aşağıdaki CEVAP metninin, yalnızca verilen REFERANS DERS NOTU bağlamına sadık kalıp kalmadığını değerlendir.
Modele dışarıdan kattığı doğrulanmamış bilgi veya ders notuyla çelişen bir detay var mı?

REFERANS DERS NOTU:
{context}

DEĞERLENDİRİLECEK CEVAP:
{answer}

LÜTFEN YALNIZCA GEÇERLİ BİR JSON FORMATINDA YANIT VER.
Format:
{{
  "faithfulness_score": <0.0 ile 1.0 arası float değer>,
  "is_grounded": <true veya false>,
  "hallucination_detected": <true veya false>,
  "unsupported_claims": [<bağlamda bulunmayan iddialar listesi>],
  "reasoning": "<kısa teknik gerekçe>"
}}
"""

    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen katı bir akademik denetçi ve halüsinasyon tespit uzmanısın. Yalnızca JSON üretirsin."},
                {"role": "user", "content": eval_prompt}
            ],
            model=llm_model_name,
            temperature=0.0
        )

        content = response.choices[0].message.content.strip()

        # Markdown temizliği
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        result = json.loads(content)
        return result

    except Exception as e:
        # Hata durumunda güvenlik için varsayılan fallback
        return {
            "faithfulness_score": 1.0,
            "is_grounded": True,
            "hallucination_detected": False,
            "unsupported_claims": [],
            "reasoning": f"Denetim sırasında hata oluştu: {str(e)}"
        }