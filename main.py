import datetime
from fastapi import FastAPI, HTTPException, UploadFile
from starlette.middleware.cors import CORSMiddleware

#from app.api.api_v1.api import api_router
from app.core.config import settings

from typing import Any, Annotated

import pathlib 
import os
from PIL import Image
import io

from fastapi.staticfiles import StaticFiles

import cv2 
import numpy as np 

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.mount("/images", StaticFiles(directory="images"), name="images")

# Set all CORS enabled origins
# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/scan")
async def root():
    now = datetime.datetime
    return {"message":"scan",
            "scan_img_url": "/images/default_01.png",
            "scan_msg_str": "Scan: Successful Scan. Outer Rim passes.",
            "scan_time_str": f"Last Scan: {now}"
            }
    
#app.include_router(api_router, prefix=settings.API_V1_STR)

@app.post("/analyze-image/")
async def upload_file(
    file: UploadFile
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

        try:
            filename = os.path.basename(file.filename)
            script_dir = os.path.dirname(os.path.abspath(os.sep))
            files_dir = os.path.abspath(os.path.join(script_dir, os.environ.get('IMAGE_UPLOAD_DIR')))
            current_permissions = os.stat(files_dir).st_mode
            os.chmod(files_dir, 0o755)
            os.makedirs(files_dir, exist_ok=True)
            filepath = os.path.join(files_dir, os.path.basename(file.filename))
        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Error with filepath: {e}")
            return {"msg":f"Error saving file: {e}"}


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
            message = "hello"

            #Load image
            image = cv2.imread(image_url)
            
            # Apply Gaussian blur to the original image
            blurred_image = cv2.GaussianBlur(image, (15, 15), 0)  # Adjust the kernel size as needed
            
            # Convert the blurred image to grayscale
            gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray_image, 50, 150)
            
            # Find contours in the edged image
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Get the area of the whole image
            image_area = gray_image.shape[0] * gray_image.shape[1]
            
            # Draw circles based on detected contours on the original image
            for contour in contours:
                # Calculate the bounding box for the contour
                x, y, w, h = cv2.boundingRect(contour)
            
                # Calculate the area covered by the bounding box
                bounding_box_area = w * h
            
                # Check if the bounding box area is at least 20% of the image area
                if bounding_box_area >= 0.2 * image_area:
                    # Fit a circle to the contour
                    if len(contour) >= 5:
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        center = (int(x), int(y))
                        radius = int(radius)
                        
                        # Calculate the area of the circle
                        circle_area = np.pi * radius**2
            
                        # Check if the circle area is at least 50% of the image area
                        if circle_area >= 0.15 * image_area:
                            # Draw the circle on the original image
                            cv2.circle(image, center, radius, (0, 255, 0), 2)  # Change (0, 255, 0) to the desired circle color
            
            # Save the resulting image with circles
            cv2.imwrite("/workspace/vision-opencv/images/ring_2_circletest.png", image)
            print(f"message: {message}")
            return message
        except openai.APIError as e:
            raise HTTPException(status_code=400, detail=f"OpenAI API Error: {e}")

    return {"msg":"Not here"}


  
