from io import BytesIO
from pdfminer.high_level import extract_text
import re


def extract_entities(pdf_bytes: bytes) -> dict:
    pdf_stream = BytesIO(pdf_bytes)
    text = extract_text(pdf_stream)

    entities = {}

    # 1. Extract Name (appears after "Herr")
    name_match = re.search(
        r"Herr\s+([A-Z][a-zA-ZäöüÄÖÜß]+\s+[A-Z][a-zA-ZäöüÄÖÜß]+)", text
    )
    if name_match:
        entities["name"] = name_match.group(1)

    # 2. Extract Bestellungsnummer (following "Bestell-Nummer" in tabular section)
    bestel_match = re.search(
        r"Bestell-Nummer\s+Artikel-\s+Nummer\s+Menge.*?\n\d+\s+(\d{6})", text, re.DOTALL
    )
    if bestel_match:
        entities["bestellnummer"] = bestel_match.group(1)

    # 3. Extract Artikelname (line after bestellnummer line)
    artikel_match = re.search(r"\d+\s+\d+\s+\d+\s+(.*?)\s+\d+,\d{2}", text)
    if artikel_match:
        entities["artikelname"] = artikel_match.group(1).strip()

    # Optional: snippet for debugging
    entities["raw_text_snippet"] = text[:1000]

    return entities
