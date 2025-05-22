from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_NAME = "gaussalgo/T5-LM-Large-text2sql-spider"
TARGET_DIR = "./local_model"

if os.path.exists(os.path.join(TARGET_DIR, "config.json")):
    print(f"✅ Model already exists at {TARGET_DIR}, skipping download.")
else:
    print(f"Downloading model and tokenizer to {TARGET_DIR}...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(TARGET_DIR)

    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.save_pretrained(TARGET_DIR)

    print("Model and tokenizer saved successfully.")
