from app.ocrs import EasyOCR


reader = EasyOCR(['es'])

resource = Path()
text = reader.read_text()
