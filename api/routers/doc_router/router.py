import sys
from typing import Optional

from fastapi import APIRouter

sys.path.append(".")

from api.db.models import Doc

router = APIRouter(prefix="/doc",tags=["doc"])


@router.post("/create")
async def create_document(
    text: Optional[str] = None
):
    Doc.create_document(None, text)
    
    return {'success': True, 'message': "Creted Document"}


@router.get("/fts")
async def full_text_search(
    text: str
):
    res = Doc.fts(text)
    return res


