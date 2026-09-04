# pdf işleme
import io
from pypdf import PdfReader


def process_pdf(file_bytes: bytes, chunk_size: int = 500) -> tuple[int, list[str]]:
    """PDF baytlarını okur, sayfa sayısını ve metin parçalarını döner."""
    pdf_stream = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_stream)
    toplam_sayfa = len(reader.pages)

    tam_metin = ""
    for sayfa in reader.pages:
        metin = sayfa.extract_text()
        if metin:
            tam_metin += metin + "\n"

    chunks = [tam_metin[i:i + chunk_size] for i in range(0, len(tam_metin), chunk_size)]
    return toplam_sayfa, chunks