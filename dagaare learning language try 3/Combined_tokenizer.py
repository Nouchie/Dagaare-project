import os
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import tiktoken
import torch.nn as nn

# Define the SentenceEmbedding class (already provided)
class SentenceEmbedding(nn.Module):
    def __init__(self, max_sequence_length, d_model, language_to_index, START_TOKEN, END_TOKEN, PADDING_TOKEN):
        super().__init__()
        self.vocab_size = len(language_to_index)
        self.max_sequence_length = max_sequence_length
        self.embedding = nn.Embedding(self.vocab_size, d_model)
        self.language_to_index = language_to_index
        self.START_TOKEN = START_TOKEN
        self.END_TOKEN = END_TOKEN
        self.PADDING_TOKEN = PADDING_TOKEN
    
    def batch_tokenize(self, batch, start_token, end_token):
        def tokenize(sentence, start_token, end_token):
            sentence_word_indices = [self.language_to_index.get(token, self.language_to_index[self.PADDING_TOKEN]) for token in sentence]
            if start_token:
                sentence_word_indices.insert(0, self.language_to_index[self.START_TOKEN])
            if end_token:
                sentence_word_indices.append(self.language_to_index[self.END_TOKEN])
            while len(sentence_word_indices) < self.max_sequence_length:
                sentence_word_indices.append(self.language_to_index[self.PADDING_TOKEN])
            return torch.tensor(sentence_word_indices)
        
        tokenized = [tokenize(sentence, start_token, end_token) for sentence in batch]
        return torch.stack(tokenized).to(self.get_device())
    
    def forward(self, x, start_token, end_token):
        x = self.batch_tokenize(x, start_token, end_token)
        x = self.embedding(x)
        pos = self.position_encoder().to(self.get_device())
        x = self.dropout(x + pos)
        return x
    
    def get_device(self):
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize the Tiktoken Tokenizer
class TiktokenTokenizer:
    def __init__(self, model_path: str):
        assert os.path.isfile(model_path), model_path
        mergeable_ranks = self.load_tiktoken_bpe(model_path)
        num_base_tokens = len(mergeable_ranks)
        special_tokens = ["", "", "", "", "", "", "", "", "", ""] + [
            f"<|reserved_special_token_{i}|>" for i in range(10, 256)
        ]
        self.special_tokens = {token: num_base_tokens + i for i, token in enumerate(special_tokens)}
        self.model = tiktoken.Encoding(
            name=os.path.basename(model_path),
            pat_str=r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+",
            mergeable_ranks=mergeable_ranks,
            special_tokens=self.special_tokens,
        )
    
    def load_tiktoken_bpe(self, model_path: str):
        # This should be the actual implementation of loading the BPE model
        # For now, we'll return an empty dictionary for demonstration
        return {}
    
    def encode(self, text: str) -> list:
        return self.model.encode(text)
    
    def decode(self, tokens: list) -> str:
        return self.model.decode(tokens)

# Combine Tokenizers
def combined_tokenize(input_text, sentence_embedding_model, tiktoken_tokenizer, start_token, end_token):
    # Step 1: Use Tiktoken tokenizer to tokenize the input text
    tiktoken_ids = tiktoken_tokenizer.encode(input_text)
    
    # Step 2: Map Tiktoken IDs to predefined dictionary and handle special tokens
    mapped_tokens = [sentence_embedding_model.language_to_index.get(str(id), sentence_embedding_model.language_to_index[sentence_embedding_model.PADDING_TOKEN]) for id in tiktoken_ids]
    
    # Step 3: Add special tokens
    if start_token:
        mapped_tokens.insert(0, sentence_embedding_model.language_to_index[sentence_embedding_model.START_TOKEN])
    if end_token:
        mapped_tokens.append(sentence_embedding_model.language_to_index[sentence_embedding_model.END_TOKEN])
    
    # Step 4: Pad the sequence to the maximum length
    while len(mapped_tokens) < sentence_embedding_model.max_sequence_length:
        mapped_tokens.append(sentence_embedding_model.language_to_index[sentence_embedding_model.PADDING_TOKEN])
    
    return torch.tensor(mapped_tokens).to(sentence_embedding_model.get_device())

# Example Usage
language_to_index = {'<PAD>': 0, '<START>': 1, '<END>': 2, 'H': 3, 'e': 4, 'l': 5, 'o': 6, ' ': 7, 'W': 8, 'r': 9, 'd': 10}
START_TOKEN = '<START>'
END_TOKEN = '<END>'
PADDING_TOKEN = '<PAD>'
max_sequence_length = 20
d_model = 50

sentence_embedding_model = SentenceEmbedding(max_sequence_length, d_model, language_to_index, START_TOKEN, END_TOKEN, PADDING_TOKEN)
tiktoken_tokenizer = TiktokenTokenizer(r"C:\Users\JASON\AppData\Local\Programs\Python\Python312\Lib\site-packages\tiktoken")

input_text = "Hello World"
combined_tokens = combined_tokenize(input_text, sentence_embedding_model, tiktoken_tokenizer, start_token=True, end_token=True)

print(combined_tokens)

