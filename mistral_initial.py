# -*- coding: utf-8 -*-
"""Mistral_initial.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b4QAFrL0H1qcCZCWZKz1sJwucY1H1e4g
"""

!pip install -q -U langchain transformers bitsandbytes accelerate

!pip install --upgrade langchain
!pip install langchain-community

import torch
from transformers import BitsAndBytesConfig
from langchain import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from huggingface_hub import login

login(token='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')

# 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
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

model_4bit = AutoModelForCausalLM.from_pretrained( "mistralai/Mistral-7B-Instruct-v0.1", device_map="auto",quantization_config=quantization_config, )
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

pipeline_inst = pipeline(
        "text-generation",
        model=model_4bit,
        tokenizer=tokenizer,
        use_cache=True,
        device_map="auto",
        max_length=2500,
        do_sample=True,
        top_k=5,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
)

llm = HuggingFacePipeline(pipeline=pipeline_inst)

template = """[INST] You are an assistant, that labels whether the given Twitch comment is toxic or not
Answer the question below in one word: toxic or non-toxic:
{question} [/INST]
"""

def generate_response(question):
  prompt = PromptTemplate(template=template, input_variables=["question","context"])
  llm_chain = LLMChain(prompt=prompt, llm=llm)
  response = llm_chain.run({"question":question})
  return response

generate_response("Are you dumb")