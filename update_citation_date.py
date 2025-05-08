"""Set the date-released field in CITATION.cff to today."""

from datetime import date

CITATION_FILE = "CITATION.cff"

lines = []
with open(CITATION_FILE, encoding="utf-8") as f:
    for line in f:
        if line.startswith("date-released:"):
            lines.append(f"date-released: {date.today()}\n")
        else:
            lines.append(line)

with open(CITATION_FILE, "w", encoding="utf-8") as f:
    f.writelines(lines)
