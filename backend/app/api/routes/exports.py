from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.exports.service import ExportService


router = APIRouter(prefix="/exports", tags=["exports"])
export_service = ExportService()


@router.get("/{session_id}")
def export_session(
    session_id: str,
    format: str = Query(default="csv", pattern="^(csv|json)$"),
    db: Session = Depends(get_db),
) -> Response:
    try:
        content, media_type = export_service.export_session(db, session_id, format)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{session_id}.{format}"'},
    )
