import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from src.logger import logger

LOCAL_MODEL_PATH = os.path.abspath("./local_model")
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH, local_files_only=True)
model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL_PATH, local_files_only=True)
model.eval()

if torch.cuda.is_available():
    model.to("cuda")


def generate(
        prompt: str,
        max_length: int = 256,
        do_sample: bool = False,
        num_return_sequences: int = 1
):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            do_sample=do_sample,
            num_return_sequences=num_return_sequences
        )
        logger.info(f"model raw output: {outputs}")
        result = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        logger.info(f"model processed output: {result}")
        return result
