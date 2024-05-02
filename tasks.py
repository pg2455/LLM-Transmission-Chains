from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from prompt_generator import TaskPromptFactory
from enums import TaskType
from base_model import BaseAPIModel
import pathlib
import pandas as pd
import random


ROOT = pathlib.Path(__file__).resolve().parent

class TaskFactory:

    @staticmethod
    def create(task_type: TaskType, llm_model_execute: BaseAPIModel, llm_model_evaluate: Optional[BaseAPIModel], **kwargs):
        if not isinstance(task_type, TaskType):
            raise ValueError("Invalid task type.")

        if task_type is TaskType.GENDER_STEREOTYPE_CONSISTENCY:
            cls = GenderStereotypeConsistencyTask
        elif task_type is TaskType.NEGATIVITY:
            cls = NegativityTask
        elif task_type is TaskType.AMBIGUITY:
            cls = AmbiguityTask
        elif task_type is TaskType.SOCIAL:
            cls = SocialTask
        elif task_type is TaskType.THREAT:
            cls = ThreatTask
        elif task_type is TaskType.MULTIPLEBIAS:
            cls = MultipleBiasTask
        else:
            raise ValueError(f"Task not recognized as a valid class: {task_type.name}")

        return cls(llm_model_execute, llm_model_evaluate, **kwargs)

class BaseTask(ABC):
    """Base class for agents."""

    @abstractmethod
    def setup(self, *args: Any, **kwargs: Any) -> Any:
        """Setup the task."""
        pass 

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Resets the agent to its initial state."""
        pass 
    
    @abstractmethod
    def evaluate(self, *args: Any, **kwargs: Any) -> Any:
        """Performs a single step of the agent."""
        pass


class BaseTelephoneGameTask(BaseTask):

    def __init__(self, task_type: TaskType, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None):
        self.prompts = TaskPromptFactory.create(task_type)
        self.llm_model_execute = llm_model_execute
        self.llm_model_evaluate = llm_model_evaluate
        self.setup()

    def setup(self):
        raise NotImplementedError("Subclasses must implement the setup method.")

    def execute(self, input_story: Optional[List[str]]):
        if input_story is None or len(input_story) == 0:
            exec_kwargs = {"input_story": self._original_story}
        else:
            exec_kwargs = {"input_story": input_story[0]}

        messages = self.prompts.get_execution_messages(**exec_kwargs)
        response = self.llm_model_execute.query(messages)
        return response.choices[0].message.content
    
    def evaluate(self, summary):
        prompt_kwargs = {
            "original_story": self._original_story,
            "phrases": self._phrases,
            "summary": summary
        }

        messages = self.prompts.get_evaluation_messages(**prompt_kwargs)
        response = self.llm_model_evaluate.query(messages)
        return response.choices[0].message.content
  

class GenderStereotypeConsistencyTask(BaseTelephoneGameTask):

    # input_files
    coding_data_RA = ROOT / "study-data/coding/Second Coder/study1_RA.xlsx"
    coding_data = ROOT / "study-data/coding/study1.xlsx"
    story_file = ROOT / "study-data/stories/kashima.txt"

    index_consistent = ['BMC', 'PMC', 'PFC', 'BFC']
    index_inconsistent = ['BMI', 'PMI', 'PFI', 'BFI']

    def __init__(self, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None):
        super().__init__(TaskType.GENDER_STEREOTYPE_CONSISTENCY, llm_model_execute, llm_model_evaluate)

    def setup(self):
        # for prompt: original story 
        self._original_story = open(str(self.story_file), 'r').read()

        # for prompt: phrases from the story
        exp_data = pd.read_excel(str(self.coding_data))
        phrases = []
        for row in exp_data.iterrows():
            x = row[1]['Unnamed: 0']

            if pd.isna(x):
                continue 

            if x in self.index_consistent or x in self.index_inconsistent:
                cat = x
                continue
            else:
                phrase = x
            phrases.append(phrase.strip())

        self._phrases = "\n".join(phrases)


class NegativityTask(BaseTelephoneGameTask):

    # input_files
    coding_data_RA = ROOT / "study-data/coding/Second Coder/study2_RA.xlsx"
    coding_data = ROOT / "study-data/coding/study2.xlsx"
    story_file = ROOT / "study-data/stories/bebbington.txt"

    POSITIVE = "POSITIVE:"
    NEGATIVE = "NEGATIVE:"
    AMBIGUOUS = "AMBIGOUS:"
    sentiments = [POSITIVE, NEGATIVE, AMBIGUOUS]

    def __init__(self, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None):
        super().__init__(TaskType.NEGATIVITY, llm_model_execute, llm_model_evaluate)

    def setup(self):
        # for prompt: original story 
        self._original_story = open(str(self.story_file), 'r').read()

        # for prompt: phrases from the story
        exp_data = pd.read_excel(str(self.coding_data))
        phrases = []
        for row in exp_data.iterrows():
            x = row[1]['Unnamed: 0']

            if pd.isna(x):
                continue 

            if x in self.sentiments:
                continue
            else:
                phrase = x
            phrases.append(phrase.strip())

        self._phrases = "\n".join(phrases)


class AmbiguityTask(BaseTelephoneGameTask):

    # input_files
    coding_data_RA = ROOT / "study-data/coding/Second Coder/study2_RA.xlsx"
    coding_data = ROOT / "study-data/coding/study2.xlsx"
    story_file = ROOT / "study-data/stories/bebbington.txt"

    POSITIVE = "POSITIVE:"
    NEGATIVE = "NEGATIVE:"
    AMBIGUOUS = "AMBIGOUS:"
    sentiments = [POSITIVE, NEGATIVE, AMBIGUOUS]

    def __init__(self, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None):
        super().__init__(TaskType.AMBIGUITY, llm_model_execute, llm_model_evaluate)

    def setup(self):
        # for prompt: original story 
        self._original_story = open(str(self.story_file), 'r').read()

        # for prompt: phrases from the story
        exp_data = pd.read_excel(str(self.coding_data))
        phrases = []
        for row in exp_data.iterrows():
            x = row[1]['Unnamed: 0']

            if pd.isna(x):
                continue 

            if x in self.sentiments:
                cat = x
                continue
            else:
                phrase = x

            if cat != self.AMBIGUOUS:
                continue
            phrases.append(phrase.strip())

        self._phrases = "\n".join(phrases)


class SocialTask(BaseTelephoneGameTask):

    # input_files
    coding_data_RA = ROOT / "study-data/coding/Second Coder/study3_RA.xlsx"
    coding_data = ROOT / "study-data/coding/study3.xlsx"
    story_file = ROOT / "study-data/stories/mesoudi.txt"

    def __init__(self, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None):
        super().__init__(TaskType.SOCIAL, llm_model_execute, llm_model_evaluate)

    def setup(self):
        # for prompt: original story 
        self._original_story = open(str(self.story_file), 'r').read()

        exp_data = pd.read_excel(str(self.coding_data))
        props = exp_data['Unnamed: 0'].iloc[1:].tolist()
        nums = exp_data['Unnamed: 1'].iloc[1:].tolist()
        self._phrases = "\n".join([f"{x}\t{y}" for x, y in list(zip(props, nums))])


class ThreatTask(BaseTelephoneGameTask):

    # input_files
    narrative_file: pathlib.Path
    lancer_file = ROOT / "study-data/stories/blaine_boyer_lancer.txt"
    flash_file = ROOT / "study-data/stories/blaine_boyer_flash.txt"
    nutane_file = ROOT / "study-data/stories/blaine_boyer_nutane.txt"

    def __init__(self, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None, **kwargs):
        study_type = kwargs['study']
        
        if study_type == "lancer":
            self.narrative_file = self.lancer_file
        elif study_type == "flash":
            self.narrative_file = self.flash_file
        elif study_type == "nutane":
            self.narrative_file = self.nutane_file
        else:
            raise ValueError(f"Unrecognized study_type : {study_type}")

        super().__init__(TaskType.THREAT, llm_model_execute, llm_model_evaluate)

    def setup(self):
        # for prompt
        narrative = open(str(self.narrative_file), "r").read()
        self.narrative, raw_statements = narrative.split("Here are the statements:")
        raw_statements = raw_statements.strip().split("\n")
        statements = []
        for raw in raw_statements:
            if not raw:
                continue

            statement = self.normalize_string(raw)
            statements.append(statement)
        
        self.statements = tuple(statements)

    
    def execute(self, statements: Optional[List[str]]):
        if statements is None or len(statements) == 0:
            statements = list(self.statements).copy()
            random.shuffle(statements)
        else:
            statements = statements[0] # it should be a list of statements
        
        exec_kwargs = {}
        exec_kwargs['statements'] = "\n".join(statements)
        exec_kwargs['narrative'] = self.narrative
        exec_kwargs['n'] = len(statements) - 1
        messages = self.prompts.get_execution_messages(**exec_kwargs)
        response = self.llm_model_execute.query(messages)
        selected_statements = response.choices[0].message.content.split("\n")
        return selected_statements
    
    def evaluate(self, summary):
        pass # No evaluation required.

    def normalize_string(self, s):
        """Normalizes string s wrt apostrophe."""
        s = s.replace('’', '')
        s = s.replace("'", '')
        return " ".join(s.split())
    

class MultipleBiasTask(BaseTelephoneGameTask):

    # input_files
    narrative_file: pathlib.Path
    muki_file = ROOT / "study-data/stories/berl_muki.txt"
    takatoro_file = ROOT / "study-data/stories/berl_takatoro.txt"

    muki_coding_file = ROOT / "study-data/coding/study5_Muki.xlsx"
    takatoro_coding_file = ROOT / "study-data/coding/study5_TakaToro.xlsx"

    def __init__(self, llm_model_execute: Optional[BaseAPIModel]=None, llm_model_evaluate: Optional[BaseAPIModel]=None, **kwargs):
        study_type = kwargs['study']
        
        if study_type == "Muki":
            self.narrative_file = self.muki_file
            self.coding_file = self.muki_coding_file
        elif study_type == "TakaToro":
            self.narrative_file = self.takatoro_file
            self.coding_file = self.takatoro_coding_file
        else:
            raise ValueError(f"Unrecognized study_type : {study_type}")

        super().__init__(TaskType.MULTIPLEBIAS, llm_model_execute, llm_model_evaluate)

    def setup(self):
        # for prompt
        self._original_story = open(str(self.narrative_file), "r").read()
        exp_data = pd.read_excel(str(self.coding_file))
        exp_data = exp_data.iloc[1:]
        exp_data = exp_data.sort_values(by=['Unnamed: 0'])
        props = exp_data['Unnamed: 0'].tolist()
        nums = exp_data['Unnamed: 1'].tolist()
        self._phrases = "\n".join([f"{x}\t{y}" for x, y in list(zip(props, nums))])

