from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)


model_name = "jyotsna2411/real-estate-new" #path/to/your/model/or/name/on/hub

modelfinetuned = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
tokenizerfinetuned = AutoTokenizer.from_pretrained(model_name)

# # Save the model and tokenizer to a local directory
# model.save_pretrained("/home/jyotsna/Virtual_Real_Estate_Agent/source/finetunedmodel/model")
# tokenizer.save_pretrained("/home/jyotsna/Virtual_Real_Estate_Agent/source/finetunedmodel/tokenizer")

# modelfinetuned = AutoModelForCausalLM.from_pretrained("/home/jyotsna/Virtual_Real_Estate_Agent/source/finetuned/model",local_files_only=True)
# tokenizerfinetuned = AutoTokenizer.from_pretrained("/home/jyotsna/Virtual_Real_Estate_Agent/source/finetuned/tokenizer")

