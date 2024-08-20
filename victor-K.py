import socket
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Configuración del bot IRC
server = "irc.libera.chat"
port = 6667
nickname = "Victor-K"
channel = "#parati"
realname = "Victor-K Bot"

# Conectar a IRC
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))

# Función para enviar mensajes al IRC
def send_message(msg):
    irc.send(bytes(msg + "\r\n", "UTF-8"))

# Realizar el handshake inicial
send_message(f"NICK {nickname}")
send_message(f"USER {nickname} 0 * :{realname}")
time.sleep(5)  # Esperar un poco antes de unirse al canal
send_message(f"JOIN {channel}")

# Cargar el modelo y el tokenizer entrenado
model_path = "./results"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Configurar el dispositivo (GPU o CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# Función para generar respuestas usando el modelo GPT-2
def generate_response(input_text):
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(inputs.input_ids, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Función principal para manejar los mensajes del IRC
def irc_bot():
    buffer = ""
    while True:
        buffer += irc.recv(2048).decode("UTF-8")
        lines = buffer.split("\r\n")
        buffer = lines.pop()

        for line in lines:
            print(line)

            if line.startswith("PING"):
                # Responder al ping para mantener la conexión viva
                send_message(f"PONG {line.split()[1]}")
            
            if "PRIVMSG" in line:
                # Extraer el mensaje y el remitente
                user = line.split("!")[0][1:]
                message = line.split("PRIVMSG")[1].split(":")[1]
                print(f"Message from {user}: {message}")

                # Comprobar si el mensaje comienza con "!pi"
                if message.startswith("!pi"):
                    # Generar respuesta usando el modelo GPT-2
                    response = generate_response(message[len("!pi "):].strip())
                    send_message(f"PRIVMSG {channel} :{response}")

# Ejecutar el bot
irc_bot()
