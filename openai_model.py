import os
from openai import OpenAI, AzureOpenAI
from typing import Dict, Any, List, Union, Optional
from messages import OpenAIMessage
from base_model import BaseAPIModel
from enums import OpenAIModelType, AzureOpenAIModelType
from configs import OpenAIChatConfig


class OpenAIModel(BaseAPIModel):
    
    def __init__(self, model_type: Union[OpenAIModelType, AzureOpenAIModelType],
                  model_config_dict: Dict[str, Any]):
        self._check_api_keys_validity()
        self._check_parameters_validity(model_config_dict)

        self._setup_client()
        self.model_type = model_type
        self.model_config_dict = model_config_dict

    def _setup_client(self) -> None:
        """Sets up the client to query the API."""
        self.url = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.key = os.getenv("OPENAI_ENDPOINT")
        self.client = OpenAI(
            api_key=self.key,
            azure_endpoint=self.url,
        )

    def _check_api_keys_validity(self) -> None:
        """Checks if the URL and token are present."""
        assert "OPENAI_API_KEY" in os.environ, KeyError(
            "OPENAI_API_KEY not found in the environment.")
        assert "OPENAI_ENDPOINT" in os.environ, KeyError(
            "OPENAI_ENDPOINT not found in the environment.")

    def _check_parameters_validity(self, parameters: Dict[str, Any]) -> None:
        """Checks if the parameters are valid."""
        try:
            OpenAIChatConfig(parameters)
        except ValueError as e:
            print("Validation error:", e)

    def query(self, messages: List[OpenAIMessage], parameters: Optional[Dict[str, Any]]=None):
        """Queries the LLM using arguments given.
        
        Args:
            messages (List[OpenAIMessage]): List of messages in the chat history.
        """
        
        if parameters is not None and len(parameters) != 0:
            self._check_parameters_validity(parameters)
            model_config = self.model_config_dict.update(parameters)
        else:
            model_config = self.model_config_dict

        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model_type.value,
            **model_config 
        )

        return response

    def format_response(self, *args: Any, **kwargs: Any):
        """Cleans up response after the API call."""
        pass 

    def failsafe_query(self, *args: Any, **kwargs: Any):
        """Retries query in case API fails."""
        pass


class AzureOpenAIModel(OpenAIModel):
    """Initializes OpenAIModel with parameters specific to Azure."""
    
    def _setup_client(self):
        """Sets up the client to query the API."""
        self.url = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("OPENAI_API_VERSION")
        self.client = AzureOpenAI(
            api_key = self.key,
            azure_endpoint = self.url,
            api_version = api_version
        )

    def _check_api_keys_validity(self):
        """Checks if the URL and token are present."""
        assert "AZURE_OPENAI_API_KEY" in os.environ, KeyError(
            "AZURE_OPENAI_API_KEY not found in the environment.")
        assert "AZURE_OPENAI_ENDPOINT" in os.environ, KeyError(
            "AZURE_OPENAI_ENDPOINT not found in the environment.")
