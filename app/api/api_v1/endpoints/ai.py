from typing import Any, Annotated
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app import controllers, models, schemas
import openai
from openai import OpenAI
from app.api import deps
from sqlalchemy.orm import Session
import pathlib 
import os
from PIL import Image
import io

router = APIRouter()


@router.post("/analyze-image/", response_model=schemas.Msg, status_code=200)
async def upload_file(
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
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
        script_dir = os.path.dirname(os.path.abspath(os.sep))
        files_dir = os.path.abspath(os.path.join(script_dir, os.environ.get('IMAGE_UPLOAD_DIR')))
        
        current_permissions = os.stat(files_dir).st_mode
        os.chmod(files_dir, 0o755)
        os.makedirs(files_dir, exist_ok=True)
        filepath = os.path.join(files_dir, os.path.basename(file.filename))

        try:
            with open(filepath, 'wb') as f:
                f.write(contents)

        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
            return {"msg":f"Error saving file: {e}"}

        finally:
            await file.close()

        try:
            image_url = f"{os.environ.get('PUBLIC_URL')}images/{filename}"
        
        except:
            raise HTTPException(status_code=400, detail="Could not get the public url of the image")
            return {"msg":f"Could not get the public url of the image"}

        try:
            message = await controllers.ai.describe_image(db, image_url)
            print(f"message: {message}")
            return message
        except openai.APIError as e:
            raise HTTPException(status_code=400, detail=f"OpenAI API Error: {e}")

    return {"msg":"Not here"}


@router.post("/analyze-image-protected/", response_model=schemas.Msg, status_code=200)
async def upload_file(
    file: UploadFile,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
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
        script_dir = os.path.dirname(os.path.abspath(os.sep))
        files_dir = os.path.abspath(os.path.join(script_dir, os.environ.get('IMAGE_UPLOAD_DIR')))
        
        current_permissions = os.stat(files_dir).st_mode
        os.chmod(files_dir, 0o755)
        os.makedirs(files_dir, exist_ok=True)
        filepath = os.path.join(files_dir, os.path.basename(file.filename))

        try:
            with open(filepath, 'wb') as f:
                f.write(contents)

        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
            return {"msg":f"Error saving file: {e}"}

        finally:
            await file.close()

        try:
            image_url = f"{os.environ.get('PUBLIC_URL')}images/{filename}"
        
        except:
            raise HTTPException(status_code=400, detail="Could not get the public url of the image")
            return {"msg":f"Could not get the public url of the image"}

        try:
            message = await controllers.ai.describe_image(db, image_url)
            print(f"message: {message}")
            return message
        except openai.APIError as e:
            raise HTTPException(status_code=400, detail=f"OpenAI API Error: {e}")

    return {"msg":"Not here"}