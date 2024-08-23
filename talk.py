from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Ruta al checkpoint más reciente
checkpoint_path = "./results"

# Cargar el modelo desde el checkpoint
model = GPT2LMHeadModel.from_pretrained(checkpoint_path)

# Cargar el tokenizador desde el modelo base original (gpt2)
tokenizer = GPT2Tokenizer.from_pretrained("datificate/gpt2-small-spanish")

def generar_respuesta(prompt, model, tokenizer, max_length=100, num_return_sequences=1):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        do_sample=True,
    )
    respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return respuesta

# Ejemplo de interacción con el modelo
prompt = "Hola, que tal?"
respuesta = generar_respuesta(prompt, model, tokenizer)
print(respuesta)
