from app.services.resume_parser import ResumeParser
from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/upload", tags=["Resume Upload"])

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    destination = UPLOAD_FOLDER / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ResumeParser.extract_text(str(destination))

    return {
        "filename": file.filename,
        "file_type": extension,
        "size": destination.stat().st_size,
        "text": extracted_text
    }