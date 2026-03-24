import sys
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
import pandas as pd

# Mount global system path reference to correctly utilize database ORM structure
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.database import engine

class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        text = str(self.texts[item])
        label = float(self.labels[item])

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True, # Critical for ignoring padding geometries
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.float)
        }

def train_bert_model():
    print("Initializing HuggingFace BERT Sentiment Engine...")
    
    # 1. Pipeline Connection via Pandas & SQL Engine directly
    print("Fetching social_posts strings natively from PostgreSQL...")
    posts_df = pd.read_sql("SELECT content, sentiment_score FROM social_posts WHERE content IS NOT NULL", engine)
    
    if len(posts_df) < 20:
        print("Error: SQL Engine returned empty posts array. Did you skip the STEP 6 generator execution?")
        return

    # Dynamic text normalization bridging
    posts_df['cleaned_content'] = posts_df['content'].astype(str).str.lower().str.replace(r'\s+', ' ', regex=True)
    
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        posts_df['cleaned_content'].tolist(), 
        posts_df['sentiment_score'].tolist(), 
        test_size=0.2, random_state=42
    )
    
    # 2. Downloading & Constructing Pre-trained Transformer Checkpoints 
    model_name = 'distilbert-base-uncased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Overriding labels to [1] for scalar linear regression (0.0 to 1.0)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)
    
    # 3. Create iterable mapping Datasets
    train_dataset = SentimentDataset(train_texts, train_labels, tokenizer)
    val_dataset = SentimentDataset(val_texts, val_labels, tokenizer)
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 4. Supply Chain optimal parameters
    training_args = TrainingArguments(
        output_dir=os.path.join(out_dir, "results"),
        num_train_epochs=3, # Efficient 3 epochs mapping for localized startup-prototyping
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir=os.path.join(out_dir, "logs"),
        logging_steps=10,
        evaluation_strategy="epoch", # Validate exactly post-epoch boundaries
        save_strategy="epoch"
    )
    
    # 5. Core Execution Graph Initialization
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )
    
    print("Beginning DistilBERT localized fine-tuning computation pass!")
    trainer.train()
    
    # 6. Serialization
    save_path = os.path.join(out_dir, "bert_sentiment_v1")
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"Custom NLP weights & tokenizer dynamically saved -> {save_path}")

if __name__ == "__main__":
    train_bert_model()
