import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split

df = pd.read_csv("../data/emails.csv")

df = df.rename(columns={"texto": "text", "categoria": "label"})
df['label'] = df['label'].map({"Produtivo": 1, "Improdutivo": 0})

print("Distribuição de classes:\n", df['label'].value_counts())

train_df, eval_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)

train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(tokenize, batched=True)
eval_dataset = eval_dataset.map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=8,
    weight_decay=0.01,
    logging_steps=10
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()

trainer.save_model("./email-classifier-model")
tokenizer.save_pretrained("./email-classifier-model")