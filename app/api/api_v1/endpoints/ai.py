from typing import Any, Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from app import controllers, models, schemas
from app.api import deps
from sqlalchemy.orm import Session
import pathlib 
import os

router = APIRouter()

#current_user: models.User = Depends(deps.get_current_active_user),

@router.post("/analyze-image/", response_model=schemas.Msg, status_code=200)
async def upload_file(
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
        pathlib.Path.home()
        directory = "images/"
        filename = "jdh_coal_pile_puzzle.png"

        file_url = f"{os.environ.get('PUBLIC_URL')}images/{filename}"

        # get image size and bounce if it is less than 512px x 512px image
        #file_url = {os.environ.get('OPENAI_TEST_IMG_URL')}
  
        if(width < 512 or height < 512):
            return {"msg":"The image size must be greater than or equal to 512px x 512px"}
        # To create a file 
        #pathlib.Path(filepath).touch() 
        
        message = await controllers.ai.describe_image(db, file_url)
        return message

    return message
