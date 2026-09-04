# services/memory_service.py
from groq.types.chat import ChatCompletionMessageParam

# Oturum bazlı geçmişi tutan sözlük: { "session_id": [mesajlar] }
SESSION_MEMORY: dict[str, list[ChatCompletionMessageParam]] = {}

def get_chat_history(session_id: str, max_messages: int = 6) -> list[ChatCompletionMessageParam]:
    """Belirli bir oturumun son N mesajı"""
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = []
    # Son 6 mesajı alıyoruz ki bağlam çok uzayıp token limitini zorlamasın
    return SESSION_MEMORY[session_id][-max_messages:]

def add_message_to_history(session_id: str, role: str, content: str):
    """Oturuma yeni mesaj gönderir"""
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = []
    SESSION_MEMORY[session_id].append({"role": role, "content": content})