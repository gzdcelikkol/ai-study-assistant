# ortam değişkenleri dosyası

import os
from dotenv import load_dotenv

load_dotenv()

grog_api_key = os.getenv("GROQ_API_KEY")
embedding_model_name = "all-MiniLM-L6-v2"
chroma_path = "./chroma_db"
llm_model_name = "openai/gpt-oss-20b"

