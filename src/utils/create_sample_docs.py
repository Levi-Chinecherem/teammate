import pandas as pd
from PyPDF2 import PdfWriter, PdfReader
import io

# Excel
df = pd.DataFrame({"Data": ["Row 1: Hello", "Row 2", "Row 3", "Row 4", "Row 5: Test Data"]})
df.to_excel("../data/sample.xlsx", index=False)

# PDF (simple text, requires external creation for now)
print("Create sample.pdf manually with text 'This is a test PDF'")

print("Sample documents created at data/")