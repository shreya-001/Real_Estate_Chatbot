
from Utils.LoadModel import modelfinetuned,tokenizerfinetuned
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)


def fine_tuned_resp(prompt):
  # global modelfinetuned,tokenizerfinetuned
  pipe = pipeline(task="text-generation", model=modelfinetuned, tokenizer=tokenizerfinetuned, max_length=50, truncation=True)
  # Generate initial text
  initial_output = pipe(f"<s>[INST] {prompt} [/INST]")
  generated_text = initial_output[0]['generated_text']
      # Remove unwanted tokens and handle incomplete sentences
  generated_text = generated_text.replace("<s>", "").replace("[INST]", "").replace("[/INST]", "").replace(prompt,"")
  sentences = generated_text.split('. ')

    # Check if last sentence has a period
  if not sentences[-1].endswith('.'):
        sentences = sentences[:-1]  # Remove the last sentence
   # Join sentences back into a string
  generated_text = '. '.join(sentences) + '.'      

  return generated_text.strip()

# # Example usage:
# prompt = "How is real estate market of Kitchener doing?"
# result = fine_tuned_resp(prompt)
# print(result)
# prompt = "How is real estate market of Toronto doing?"
# result = fine_tuned_resp(prompt)
# print(result)