from abc import ABC, abstractmethod
from typing import Any, Optional

class AIPlatform(ABC):
    """
    Abstract base class for AI platforms.
    """

    @abstractmethod
    def chat(self, prompt: str) -> Optional[str]:
        """
        Send a prompt to the AI model and receive a response.
        
        :param prompt: The input text to send to the AI model.
        :return: The response text from the AI model.
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict[str, Any]:
        """
        Retrieve information about the AI model being used.
        
        :return: A dictionary containing model information.
        """
        pass
