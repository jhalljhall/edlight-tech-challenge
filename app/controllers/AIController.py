from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
import os
from fastapi import UploadFile
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
        print(f"image: {image_url}")
        try:
            response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
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
                        "url": image_url,
                    },
                    },
                ],
                }
            ],
            max_tokens=500,
            )
            return {"msg": response.choices[0].message.content}
            # Handling different HTTP responses
            if response.status_code == 200:
                return {"msg": response.choices[0].message.content}
            elif 400 <= response.status_code < 500:
                return {"msg": "Client error occurred."}
            elif 500 <= response.status_code < 600:
                return {"msg": "Server error occurred."}
            else:
                return {"msg": "Unexpected error occurred."}

        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return {"msg": f"OpenAI API returned an API Error: {e}"}
            
        except openai.APIConnectionError as e:
            #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
            return {"msg": f"Failed to connect to OpenAI API: {e}"}
            
        except openai.RateLimitError as e:
            #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
            return {"msg": f"OpenAI API request exceeded rate limit: {e}"}
            
        return {"msg":"Unexpected error occurred."}

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')       

ai = AIController()
