from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
from datasets import load_dataset
from transformers import Trainer, TrainingArguments
import torch

TRAIN_BASE = False

paths = ["dagaare_dict.txt"]

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"])

    tokenizer.save_model("tokenizer")


inp = "print('Kaara lɛ nensaala.')"

tokenizer = GPT2Tokenizer.from_pretrained('tokenizer')

# Add special tokens without splitting them during tokenization
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>",
})


t = tokenizer.encode(inp)

print(t)

print(tokenizer.decode(t))

config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,
)

model = GPT2LMHeadModel(config)

dataset = load_dataset("text", data_files=paths)

def encode(example):
    text = example["text"]  # Extract the text from the dictionary
    encoded = tokenizer(text, padding=True, truncation=True, return_tensors="pt", max_length=1024)
    
    # Convert the input_ids and attention_mask to float32
    encoded["input_ids"] = encoded["input_ids"].squeeze(0).to(torch.float32)  # Remove batch dimension and convert to float32
    encoded["attention_mask"] = encoded["attention_mask"].squeeze(0).to(torch.float32)  # Remove batch dimension and convert to float32
    
    return encoded

dataset = dataset.map(encode)

# Define a custom collate function without padding
def my_collate_fn(examples):
    input_ids = torch.stack([example["input_ids"] for example in examples])
    attention_mask = torch.stack([example["attention_mask"] for example in examples])
    return {"input_ids": input_ids, "attention_mask": attention_mask}

training_args = TrainingArguments(
    output_dir=r"C:\Users\JASON\Desktop\programming\Dagaare project\dagaare_learning_language",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=10,
    save_steps=100,
    save_total_limit=2,
    prediction_loss_only=True,
    remove_unused_columns=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=my_collate_fn,
    train_dataset=dataset["train"],
)

trainer.train()

trainer.save_model("Dagaare_trainer")
