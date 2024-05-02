from enum import Enum


class OpenAIModelType(Enum):
    """Models are specified here: https://platform.openai.com/docs/models/overview"""
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"
    GPT_4_32K = "gpt-4-32k"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"

    @property
    def token_limit(self) -> int:
        """Returns the maximum token limit for a given model."""
        if self is OpenAIModelType.GPT_3_5_TURBO:
            return 16385
        elif self is OpenAIModelType.GPT_3_5_TURBO_INSTRUCT:
            return 16385
        elif self is OpenAIModelType.GPT_4_32K:
            return 32768
        elif self is OpenAIModelType.GPT_4:
            return 8192
        elif self is OpenAIModelType.GPT_4_TURBO:
            return 128000
        elif self is OpenAIModelType.GPT_4_TURBO_PREVIEW:
            return 128000
        else:
            raise ValueError(f"Unexpected model type: {self}.")


class AzureOpenAIModelType(Enum):
    GPT_3_5_TURBO = "gpt-35-turbo"
    GPT_3_5_TURBO_INSTRUCT = "gpt-35-turbo-instruct"
    GPT_4_VISION = "gpt-4-vision"
    GPT_4 = "gpt-4"
    GPT_4_NO_FILTERS = "gpt-4-no-filters"
    GPT_4_TURBO = "gpt-4-turbo-1106"
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"

    @property
    def token_limit(self) -> int:
        """Returns the maximum token limit for a given model."""
        if self is AzureOpenAIModelType.GPT_3_5_TURBO:
            return 16385
        elif self is AzureOpenAIModelType.GPT_3_5_TURBO_INSTRUCT:
            return 16385
        elif self is AzureOpenAIModelType.GPT_4_VISION:
            return 8192
        elif self is AzureOpenAIModelType.GPT_4:
            return 8192
        elif self is AzureOpenAIModelType.GPT_4_NO_FILTERS:
            return 8192
        elif self is AzureOpenAIModelType.GPT_4_TURBO:
            return 128000
        elif self is AzureOpenAIModelType.GPT_4_TURBO_PREVIEW:
            return 128000
        else:
            raise ValueError(f"Unexpected model type: {self}.")



class EmbeddingModelType(Enum):
    """Models are specified here: https://platform.openai.com/docs/models/overview"""
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA = "text-embedding-ada-002"

    @property
    def output_dim(self) -> int:
        if self is EmbeddingModelType.TEXT_EMBEDDING_3_LARGE:
            return 3072
        elif self is EmbeddingModelType.TEXT_EMBEDDING_3_SMALL:
            return 1536
        elif self is EmbeddingModelType.TEXT_EMBEDDING_ADA:
            return 1536
        else:
            raise ValueError(f"Unknown model type: {self}.")


class OpenAIBackendRole(Enum):
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"


class TaskType(Enum):
    TELEPHONE_GAME = "base_telephone_game"
    GENDER_STEREOTYPE_CONSISTENCY = "gender_stereotype_consistency"
    NEGATIVITY = "negativity"
    AMBIGUITY = "ambiguity"
    SOCIAL = "social"
    THREAT = "threat"
    MULTIPLEBIAS = "multiple_bias"
