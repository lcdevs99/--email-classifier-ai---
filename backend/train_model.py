import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split

# 1. Carregar dataset
df = pd.read_csv("../data/emails.csv")

# Renomear colunas para o formato esperado
df = df.rename(columns={"texto": "text", "categoria": "label"})
df['label'] = df['label'].map({"Produtivo": 1, "Improdutivo": 0})

# Verificar balanceamento
print("Distribuição de classes:\n", df['label'].value_counts())

# 2. Dividir em treino e validação (estratificado para manter proporção)
train_df, eval_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)

train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

# 3. Tokenização
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(tokenize, batched=True)
eval_dataset = eval_dataset.map(tokenize, batched=True)

# 4. Modelo
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# 5. Configuração de treino (sem evaluation_strategy/save_strategy)
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=8,   # aumentei para 8 épocas
    weight_decay=0.01,
    logging_steps=10
)

# 6. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

# 7. Treinar
trainer.train()

# 8. Salvar modelo
trainer.save_model("./email-classifier-model")
tokenizer.save_pretrained("./email-classifier-model")