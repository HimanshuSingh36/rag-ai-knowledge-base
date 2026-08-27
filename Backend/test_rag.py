from pathlib import Path

from ingest import ingest_pdf


pdf_path = Path(__file__).parent / "Himanshu_Singh_Resume.pdf"

pdf_bytes = pdf_path.read_bytes()

result = ingest_pdf(
    pdf_bytes=pdf_bytes,
    filename=pdf_path.name,
)

print("\nResult:")
print(result)