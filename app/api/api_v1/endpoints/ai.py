from typing import Any, Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from app import controllers, models, schemas
from app.api import deps
from sqlalchemy.orm import Session
import pathlib 

router = APIRouter()

#current_user: models.User = Depends(deps.get_current_active_user),

@router.post("/analyze-image/", response_model=schemas.Msg, status_code=201)
async def uploadfile(
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    
) -> Any:
    """
    Retrieve Image Description.
    """
    if not file:
        return "No file provided"
    else:
        # path of this script 
        directory = "/images/"
        filepath = directory + file.filename

        # To create a file 
        pathlib.Path(filepath).touch() 
        message = await controllers.ai.describe_image(db, filepath)
        return message

    return message
