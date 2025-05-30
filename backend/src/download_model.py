from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
from src.logger import logger

MODEL_NAME = "gaussalgo/T5-LM-Large-text2sql-spider"
TARGET_DIR = "./local_model"

logger.info("checking for model availability")
if os.path.exists(os.path.join(TARGET_DIR, "config.json")):
    logger.info(f"✅ Model already exists at {TARGET_DIR}, skipping download.")
else:
    logger.info(f"Downloading model and tokenizer to {TARGET_DIR}...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(TARGET_DIR)

    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.save_pretrained(TARGET_DIR)

    logger.info("Model and tokenizer saved successfully.")
