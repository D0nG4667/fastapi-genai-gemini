import os
from typing import Any, Optional
from .base import AIPlatform
from google import genai
from google.genai import types


class Gemini(AIPlatform):
    """
    Gemini AI platform implementation.
    """

    def __init__(self, api_key: Optional[str], system_prompt: Optional[str] = None):
        """
        Initialize the Gemini AI platform with the provided API key.

        :param api_key: The API key for authenticating with the Gemini AI service.
        """
        self.api_key = api_key
        self.system_prompt = system_prompt
        if not self.api_key:
            raise ValueError(
                "API key must be provided for Gemini AI platform.")
        # Configure the Gemini AI client with the API key
        self.client: genai.Client = genai.Client(api_key=api_key)
        # Initialize the generative model
        self.model: str = "gemini-2.5-flash-preview-05-20"

    def chat(self, prompt: str) -> Optional[str]:
        """
        Send a prompt to the Gemini AI model and receive a response.        
        :param prompt: The input text to send to the AI model.
        :return: The response text from the AI model.
        
        """

        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"
        response: types.GenerateContentResponse = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_text(text=prompt),
            ],
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    )
                ]
            ),
        )
        return response.text

    def get_model_info(self) -> dict[str, Any]:
        """
        Retrieve information about the Gemini AI model being used.
        :return: A dictionary containing model information.
        """
        if not self.model:
            raise ValueError("Model name is not set.")
        return {
            "model_name": self.model,
            "description": "Gemini AI model for text generation",
        }
