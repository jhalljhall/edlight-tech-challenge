from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
import os
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv
import requests
import base64
import openai
from openai import OpenAI
import json
from PIL import Image
import io

class AIController():
    async def describe_image(self, db: Session, image_url: str) -> str:
        client = OpenAI()
        print(image_url)
        messages = [
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "What is in this image?",
                        },
                        {
                        "type": "image_url",
                            "image_url": {
                                "url": f"{image_url}",
                            },
                        },
                    ],
                }
            ]
        print(messages)
        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
            max_tokens=1000,
            )

            return {"msg": response.choices[0].message.content}
            
        except openai.APIError as e:
            raise HTTPException(status_code=400, detail=f"OpenAI API Error: {e}")
            return {"msg": f"OpenAI API Error: {e}"}

        except openai.APIConnectionError as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API Connection Error: {e}")
            return {"msg": f"OpenAI API Connection Error: {e}"}
            
        except openai.RateLimitError as e:
            raise HTTPException(status_code=429, detail=f"OpenAI API request exceeded rate limit: {e}")
            return {"msg": f"OpenAI API request exceeded rate limit: {e}"}

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')       

ai = AIController()
