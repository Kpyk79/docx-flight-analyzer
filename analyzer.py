from docx import Document
from datetime import datetime
from collections import defaultdict
import re

group_map = {
    "Кодима": "1. Кодима", "Шершенці": "1. Кодима", "Загнітків": "1. Кодима",
    "Станіславка": "2. Станіславка", "Тимкове": "2. Станіславка", "Чорна": "2. Станіславка",
    "Окни": "3. Окни", "Ткаченкове": "3. Окни", "Гулянка": "3. Окни", "Новосеменівка": "3. Окни",
    "Великокомарівка": "4. Великокомарівка", "Павлівка": "4. Великокомарівка",
    "Велика Михайлівка": "5. Велика Михайлівка", "Гребеники": "5. Велика Михайлівка", "Слов’яносербка": "5. Велика Михайлівка",
    "Степанівка": "6. Степанівка", "Лучинське": "6. Степанівка", "Кучурган": "6. Степанівка", "Лиманське": "6. Степанівка"
}

def analyze_doc(path: str):
    total_flights = defaultdict(int)
    evening_flights = defaultdict(int)
    doc = Document(path)

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            cell_text = ' '.join(cells)

            found_group = None
            for name, group in group_map.items():
                if re.search(fr"\b{name}\b", cell_text, re.IGNORECASE):
                    found_group = group
                    break
            if not found_group:
                continue

            time_matches = re.findall(r"\b\d{1,2}:\d{2}\b", cell_text)
            if time_matches:
                try:
                    t = datetime.strptime(time_matches[0], "%H:%M")
                    total_flights[found_group] += 1
                    if t.hour >= 18:
                        evening_flights[found_group] += 1
                except Exception:
                    continue

    return {
        "total": dict(sorted(total_flights.items())),
        "evening": dict(sorted(evening_flights.items()))
    }
