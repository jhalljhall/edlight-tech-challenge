from typing import Any, Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from app import controllers, models, schemas
from app.api import deps
from sqlalchemy.orm import Session
import pathlib 

router = APIRouter()

@router.post("/analyze-image/", response_model=schemas.Msg, status_code=201)
async def read_users(
    db: Session = Depends(deps.get_db),
    file: UploadFile | None = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Image Description.
    """
    if not file:
        return "No upload file sent"
    else:
        #store the file
        image_url = ""

        # path of this script 
        directory = "/images"
        filepath = directory + file.filename

        # To create a file 
        pathlib.Path(filepath).touch() 
        message = await controllers.ai.describe_image(db, image_url)
        return message

    return message
