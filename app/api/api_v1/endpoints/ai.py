from typing import Any, Annotated
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app import controllers, models, schemas
from app.api import deps
from sqlalchemy.orm import Session
import pathlib 
import os
from PIL import Image
import io

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
        return {"msg":"No File provided"}
    else:
        #try:
        contents = await file.read()
        file_size = len(contents)

        if(file_size == 0):
            raise  HTTPException(status_code=400, detail="Image could not be read")
            return {"msg":"Image could not be read"}
        
        size_max = 5 * 1024 * 1024
        size_min = 1 * 1024 * 1024

        if file_size > size_max:
            raise HTTPException(status_code=413, detail="File size exceeds 5 MB limit")
            return {"msg":"File size exceeds 5 MB limit"}
        
        if file_size < size_min:
            raise HTTPException(status_code=412, detail="File size needs to be larger than 1 MB")
            return {"msg":"File size needs to be larger than 1 MB"}

        image = Image.open(io.BytesIO(contents))

        if image.width < 512 or image.height < 512:
            raise HTTPException(status_code=400, detail="Image dimensions are smaller than 512x512 pixels")
            return {"msg":"Image dimensions are smaller than 512x512 pixels"}

        filename = os.path.basename(file.filename)
        script_directory = os.path.dirname(os.path.abspath(os.sep))
        files_directory = os.path.abspath(os.path.join(script_directory, os.environ.get('IMAGE_UPLOAD_DIR')))
        current_permissions = os.stat(files_directory).st_mode
        os.chmod(files_directory, 0o755)
        os.makedirs(files_directory, exist_ok=True)
        filepath = os.path.join(files_directory, os.path.basename(file.filename))

        try:
            with open(filepath, 'wb') as f:
                f.write(contents)

        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

        finally:
            await file.close()

        try:
            image_url = f"{os.environ.get('PUBLIC_URL')}images/{filename}"
            print(f"image_url: {image_url}")
        
        except:
             raise HTTPException(status_code=400, detail="Could not get the public url of the image")
        
        try:
            message = await controllers.ai.describe_image(db, image_url)
            print(f"message: {message}")
            return message
        except:
            raise HTTPException(status_code=400, detail="Could not describe the image")

    return {"msg":"Not here"}