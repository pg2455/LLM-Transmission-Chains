"""Defines the base class for calling LLM through APIs."""

import abc
from typing import Any


class BaseAPIModel(abc.ABC):
    """An abstract base class for calling LLMs through API."""

    @abc.abstractmethod
    def _setup_client(self, *args: Any, **kwargs: Any):
        """Sets up the client to query the API."""
        pass

    @abc.abstractmethod
    def _check_api_keys_validity(self, *args: Any, **kwargs: Any):
        """Checks if the URL and token are present."""
        pass

    @abc.abstractmethod
    def _check_parameters_validity(self, *args: Any, **kwargs: Any):
        """Checks if the parameters are valid."""
        pass

    @abc.abstractmethod
    def query(self, *args: Any, **kwargs: Any):
        """Queries the LLM using arguments given."""
        pass

    @abc.abstractmethod
    def format_response(self, *args: Any, **kwargs: Any):
        """Cleans up response after the API call."""
        pass

    @abc.abstractmethod
    def failsafe_query(self, *args: Any, **kwargs: Any):
        """Retries query in case API fails."""
        pass

