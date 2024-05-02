from dataclasses import dataclass
from enums import OpenAIBackendRole

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam

OpenAIMessage = ChatCompletionMessageParam
OpenAISystemMessage = ChatCompletionSystemMessageParam
OpenAIUserMessage = ChatCompletionUserMessageParam
OpenAIAssistantMessage = ChatCompletionAssistantMessageParam


@dataclass
class BaseMessage:
    """
    Base class for message objects.

    Args:
        role_name (str): 
    """
    role_name: str
    role_type: OpenAIBackendRole
    content: str


