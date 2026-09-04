# schemas/flashcard.py
from pydantic import BaseModel

class GenerateFlashcardsRequest(BaseModel):
    topic: str = "Tüm Notlar"
    card_count: int = 5

class FlashcardItem(BaseModel):
    front: str  # Kartın ön yüzü (Soru veya Kavram)
    back: str   # Kartın arka yüzü (Cevap veya Tanım)

class FlashcardsResponse(BaseModel):
    topic: str
    total_cards: int
    flashcards: list[FlashcardItem]
    anki_csv_format: str