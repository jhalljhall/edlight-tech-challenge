from typing import Any, Dict, Optional, Union
import os
from dotenv import load_dotenv
import requests
import base64
from sqlalchemy.orm import Session
from openai import OpenAI

class AIController():
    async def describe_image(self, db: Session, *, image_url: str) -> str:
        client = OpenAI()
        try:
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                        {
                            "type": "text",
                            "text": "What’s in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": {image_url}
                            }
                        }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            # use api key from .env
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ.get('OPENAI_KEY')}"
            }
            response = requests.post(f"{os.environ.get('OPENAI_API_URL')}{os.environ.get('OPENAI_CHAT_PATH')}", headers=headers, json=payload)
            return response.choices[0].message.content
        except:
            #exception
            return "An error occurred."
        # Function to encode the image
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


ai = AIController()
