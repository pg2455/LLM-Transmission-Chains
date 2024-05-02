#!/usr/bin/env python

from distutils.core import setup

setup(name='llm_models',
      version='1.0',
      description='LLM Evolution',
      py_modules=['enums', 'configs', 'analysis', 'prompt_generator', 
                  'base_model', 'openai_model', 'utils', 'messages', 'node']
     )