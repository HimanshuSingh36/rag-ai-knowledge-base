from flask import Blueprint, request, jsonify
from ingest import ingest_pdf

documens_bp = Blueprint("documents", __name__)


@documens_bp.post("/api/documents")
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No files selected"}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Currently only pdf files are allowed"}), 400

    try:
        pdf_bytes = file.read()

        result = ingest_pdf(
            pdf_bytes=pdf_bytes,
            filename=file.filename,
        )

        return (
            jsonify(
                {
                    "message": "PDF processed and indexed successfully",
                    "document_id": result["document_id"],
                    "filename": result["filename"],
                    "pages": result["pages"],
                    "chunks": result["chunks"],
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500
