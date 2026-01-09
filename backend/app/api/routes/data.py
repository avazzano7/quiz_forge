from fastapi import APIRouter, HTTPException
from pathlib import Path

router = APIRouter(prefix="/data", tags=["data"])

DATA_DIR = Path("data")

@router.get("/files")
def list_data_files():
    if not DATA_DIR.exists():
        return {"files": []}

    files = [f.name for f in DATA_DIR.iterdir() if f.is_file()]
    return {"files": files}
