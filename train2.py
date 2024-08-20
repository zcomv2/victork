from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# 1. Cargar el modelo y el tokenizer en español
#model_name = "gpt2"
model_name = "datificate/gpt2-small-spanish"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# 2. Preparar los datos
def load_dataset(file_path, tokenizer):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128
    )

def load_data_collator(tokenizer):
    return DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

train_path = "dataset-espanish.txt"  # Archivo de texto en español para entrenar
train_dataset = load_dataset(train_path, tokenizer)
data_collator = load_data_collator(tokenizer)

# 3. Configurar los parámetros de entrenamiento
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
)

# 4. Entrenar el modelo
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()

# Guardar el modelo entrenado
trainer.save_model("./results")
tokenizer.save_pretrained("./results")
