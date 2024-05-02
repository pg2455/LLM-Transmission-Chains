from dataclasses import dataclass
from enums import TaskType, OpenAIBackendRole
from messages import OpenAIMessage
from typing import Set, List, Any, Optional, Dict
import re
from abc import ABC

class TaskPromptFactory:

    @staticmethod
    def create(task_type: TaskType):
        if not isinstance(task_type, TaskType):
            raise ValueError("Invalid task type.")

        if task_type is TaskType.GENDER_STEREOTYPE_CONSISTENCY:
            return GenderStereotypeConsistencyTaskPrompt()
        elif task_type is TaskType.NEGATIVITY:
            return NegativityTaskPrompt()
        elif task_type is TaskType.AMBIGUITY:
            return AmbguityResolutionTaskPrompt()
        elif task_type is TaskType.SOCIAL:
            return SocialTaskPrompt()
        elif task_type is TaskType.THREAT:
            return ThreatTaskPrompt()
        elif task_type is TaskType.MULTIPLEBIAS:
            return MultipleBiasTaskPrompt()
        else:
            raise ValueError(f"Task Prompt not recognized: {task_type.name}")


class TextPrompt:
    
    def __init__(self, string):
        self.str = string 

    @property
    def key_words(self) -> Set[str]:
        return set(re.findall(r'{([^}]*)}', self.str))
    
    def format(self, **kwargs) -> 'TextPrompt':
        default_kwargs = {key: '{' + f'{key}' + '}' for key in self.key_words}
        default_kwargs.update(kwargs)
        return self.str.format(**kwargs)

@dataclass
class ChatPrompt:
    system_prompt: TextPrompt 
    user_prompt: TextPrompt

    def get_messages(self, **kwargs):
        return [
            {
                "role" : OpenAIBackendRole.SYSTEM.value,
                "content": self.system_prompt.format(**kwargs)
            },
            {
                "role": OpenAIBackendRole.USER.value,
                "content": self.user_prompt.format(**kwargs)
            }
        ]


class TaskPrompt(ABC):

    task_system_prompt: TextPrompt
    task_user_prompt: TextPrompt
    eval_system_prompt: TextPrompt
    eval_user_prompt: TextPrompt

    def __init__(self):

        self.execution_prompt = ChatPrompt(
            system_prompt=self.task_system_prompt, 
            user_prompt=self.task_user_prompt
        )

        self.evaluation_prompt = ChatPrompt(
            system_prompt=self.eval_system_prompt, 
            user_prompt=self.eval_user_prompt
        )


    def get_execution_messages(self, **kwargs: Optional[Dict[str, str]]) -> List[OpenAIMessage]:
        return self.execution_prompt.get_messages(**kwargs)

    def get_evaluation_messages(self, **kwargs: Optional[Dict[str, str]]) -> List[OpenAIMessage]:
        return self.evaluation_prompt.get_messages(**kwargs)


class BaseTelephoneGamePrompt(TaskPrompt):

    # task prompts
    task_system_prompt = TextPrompt(
        "You are an expert in summarizing stories to make them shorter. If necessary, you can omit some information. Only output the summary."
    )

    task_user_prompt = TextPrompt("{input_story}")

    # evaluation prompts
    eval_system_prompt = TextPrompt("""

You are an evaluator tasked to determine which phrases from an original text appear in its summarized version. Follow these instructions for completing your task:

1. Examine the List of Phrases: Carefully review the list provided under the heading <PHRASES>. Each item represents a distinct phrase extracted from the original text.
2. Read the Summary: Go through the summarized content that begins with <SUMMARY>. Your objective is to identify correspondences between the summary and the list of phrases.
3. Identify and Select Appropriate Phrases: Your task is to select only those phrases from <PHRASES> that are clearly reflected in the summary. Be diligent and ensure that each chosen phrase can genuinely be inferred from the summarized text.
4. Avoid Over-Attribution: Be conservative in your approach to selecting phrases. Avoid attributing any phrase to the summary unless you are certain of its relevance and presence in the text.
5. Output the Selected Phrases: List each selected phrase on a new line in your output. Ensure clarity and accuracy in your selections.
Your ouput should only contain phrases.
Your output should contain one phrase per line.

<PHRASES>:
{phrases}

    """)

    eval_user_prompt = TextPrompt("<SUMMARY>: {summary}")


class AmbguityResolutionTaskPrompt(BaseTelephoneGamePrompt):

    eval_system_prompt = TextPrompt("""
    You are an evaluator tasked with identifying which phrases from the original text are included in a summarized version of that text.
    You are also needed to tell whether the phrase as present in the summary can be interpreted as POSITIVE, NEGATIVE, or NEUTRAL phrase.
    You will be given phrases from a story and a corresponding summary starting with <SUMMARY>.
    Your task is to output only the phrases from <PHRASES> that are contained in the summary.
    Your output should contain one phrase per line in the following format: <SELECTED_PHRASE>\t:<INFERRED_TONE>
    <INFERRED_TONE> should be one of the three categories: POSITIVE, NEGATIVE, NEUTRAL.
    Exercise caution to avoid over-attributing the phrases. Only pick a phrase if you are sure it can be inferred from the summary.

    <PHRASES>:
    {phrases}

    """)


class SocialTaskPrompt(BaseTelephoneGamePrompt):

    eval_system_prompt = TextPrompt("""
You have been assigned the role of an evaluator, with the primary responsibility of determining which propositions from a given list are included in a summary. Below are the steps and guidelines to follow:

Review the Proposition List: First, carefully examine the list of propositions provided under the section labeled `<PROPOSITIONS>`. Each proposition is formatted as `<NUMBER>\t<PROPOSITION>`. Note that some propositions include references to other propositions through their numbers.

Read the Summary: Next, read the summary that starts with `<SUMMARY>`. Your task is to identify which propositions from the list are reflected in the summary.

Match Propositions to Summary Content: Identify and match each proposition to the content of the summary. Be meticulous in ensuring that a proposition can clearly be inferred from the summary before selecting it.

Avoid Over-Attribution: Exercise caution to prevent over-attributing propositions. Only include a proposition number in your output if you are confident it is supported by the summary content.
                                    
<PROPOSITIONS>
{phrases}
                                    
Output the Numbers: For each proposition that is included in the summary, output **ONLY** the number associated with that proposition. Write each number on a new line.
    """)

class ThreatTaskPrompt(BaseTelephoneGamePrompt):
    task_system_prompt = TextPrompt("""
    """)
    # You are a helpful friend. You will be presented with statements about a product. 
    # You are required to select some specified number of those statements that you would like your friend to know.
    # You should only output the statement without adding anything extra.


    # You are a helpful friend. You will be presented with statements about a product. 
    # You are evaluating a series of statements about a product.
    # You are required to select some specified number of those statements that you would like your friend to know.
                                    
    # Here are your instructions for carrying out this task effectively:

    # Review the Statements: You will be presented with various statements describing different aspects of a product.
    # Output the Statements: List each chosen statement **exactly** as it appears. Ensure that your output includes only the statement itself, without any additional comments or modifications or itemization.

    task_user_prompt = TextPrompt("""
        {narrative}
                                    
        Please select {n} statements from the following:
        {statements}   
        Ensure that your output includes only the statement itself, without any additional comments or modifications or itemization.     
   """)
        # List each of the {n} chosen statement **exactly** as it appears in the statements above. 
        # Ensure that your output includes only the statement itself, without any additional comments or modifications or itemization.     



GenderStereotypeConsistencyTaskPrompt = BaseTelephoneGamePrompt
NegativityTaskPrompt = BaseTelephoneGamePrompt
MultipleBiasTaskPrompt = SocialTaskPrompt
