from typing import Any, Optional, Sequence, Dict, Union, List
from dataclasses import dataclass, field, asdict

@dataclass(frozen=True)
class OpenAIChatConfig:
    """Defines the parameters for OpenAIAPI.

    Descriptions of parameters from: https://platform.openai.com/docs/api-reference/chat/create

    Args:
        temperature (float, optional, default: 1): What sampling temperature to use, between 
            0 and 2. Higher values like 0.8 will make the output more random, 
            while lower values like 0.2 will make it more focused and deterministic.

        top_p (float, optional, default: 1): An alternative to sampling with temperature, 
            called nucleus sampling, where the model considers the results of the 
            tokens with top_p probability mass. So 0.1 means only the tokens 
            comprising the top 10% probability mass are considered.

            We generally recommend altering this or `temperature` but not both.
        
        n (int, optional, default: 1) How many chat completion choices to generate 
            for each input message. Note that you will be charged based on the number 
            of generated tokens across all of the choices. Keep `n` as 1 to minimize costs.
        
        stream (bool, optional, default: False) If set, partial message deltas will
            be sent, like in ChatGPT. Tokens will be sent as data-only server-sent 
            events as they become available, with the stream terminated by a 
            data: [DONE] message.

        stop (str or list, optional, default: []) Up to 4 sequences where the
            API will stop generating further tokens.
        
        max_tokens (int, optional, default: None): he maximum number of tokens to generate
            in the chat completion. The total length of input tokens and
            generated tokens is limited by the model's context length.
        
        presence_penalty (float [-2, 2], optional, default: 0) Positive values 
            penalize new tokens based on whether they appear in the text so far, 
            increasing the model's likelihood to talk about new topics.
        
        frequency_penalty (float [-2, 2], optional, default: 0) Positive values penalize 
            new tokens based on their existing frequency in the text so far, 
            decreasing the model's likelihood to repeat the same line verbatim.
        
        logit_bias (dict, optional, default: {}): Modify the likelihood of specified tokens
            appearing in the completion. Accepts a json object that maps tokens
            (specified by their token ID in the tokenizer) to an associated
            bias value from :obj:`-100` to :obj:`100`. Mathematically, the bias
            is added to the logits generated by the model prior to sampling.
            The exact effect will vary per model, but values between` -1`
            and `1` should decrease or increase likelihood of selection;
            values like `-100` or `100` should result in a ban or
            exclusive selection of the relevant token.
        
        user (str, optional, default: "") A unique identifier representing your 
            end-user, which can help OpenAI to monitor and detect abuse.
        
        seed (int, optional, default: None) This feature is in Beta. If specified, 
            our system will make a best effort to sample deterministically, such 
            that repeated requests with the same seed and parameters should return 
            the same result. Determinism is not guaranteed, and you should refer 
            to the system_fingerprint response parameter to monitor changes in 
            the backend.
        
        logprobs (bool, optional, default: False) Whether to return log probabilities 
            of the output tokens or not. If true, returns the log probabilities 
            of each output token returned in the content of message.

        top_logprobs (int, optional, default: 0) Valid only if logprobs is True.
            An integer between 0 and 20 specifying the number of most likely tokens 
            to return at each token position, each with an associated log probability. 

        response_format (dict(str, str), optional, default: {}) An object specifying the 
            format that the model must output. Compatible with GPT-4 Turbo and 
            all GPT-3.5 Turbo models newer than gpt-3.5-turbo-1106.

            Setting to { "type": "json_object" } enables JSON mode, which guarantees 
            the message the model generates is valid JSON.

            Important: when using JSON mode, you must also instruct the model to 
            produce JSON yourself via a system or user message.

    """

    temperature: float = 0.2  # openai default: 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[Union[str, Sequence[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    logit_bias: Dict[str, float] = field(default_factory=dict)
    user: str = ""
    seed: Optional[int] = None
    logprobs: bool = False
    top_logprobs: int = 1
    response_format: Optional[Dict[str, str]] = None


# @dataclass(frozen=True)
# def ToolUsingOpenAIConfig(OpenAIConfig):
#     """Defines parameters necessary for using GPT with tools.
    
#     Args:
#         tools (list, optional, default: []) A list of tools the model may call. 
#             Currently, only functions are supported as a tool. 
#             Use this to provide a list of functions the model may generate JSON 
#             inputs for. A max of 128 functions are supported.

#         tool_choice (str, optional, default: none or auto) Controls which (if any) function is called by the model. 
#             none means the model will not call a function and instead generates a message. 
#             auto means the model can pick between generating a message or calling a function. 
#             Specifying a particular function via 
#             {"type": "function", "function": {"name": "my_function"}} forces the 
#             model to call that function.

#             none is the default when no functions are present. auto is the default 
#             if functions are present.  
#     """
#     tools: List[Dict[str, Any]] = field(default_factory=list)
#     tool_choice: Optional[str] = "none"


OPENAI_API_PARAMS = {param for param in asdict(OpenAIChatConfig()).keys()}
# OPENAI_API_PARAMS_WITH_FUNCTIONS = {
#     param for param in asdict(ToolUsingOpenAIConfig()).keys()
# }