import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Configuração de conexão com o servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # NOVO SOCKET TCP IP É CRIADO TCP
client.connect(("127.0.0.1", 3308)) # SE CONECTA NO SERVIDOR E PORTA

# Solicita o apelido do usuário
nickname = simpledialog.askstring("Nickname", "Digite seu apelido:")

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            # Verificar se a mensagem indica que o próprio usuário entrou no chat
            if message == f"{nickname} entrou no chat!":
                message = "Você entrou no chat!"  # Alterar a mensagem para o próprio usuário

            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, message + "\n")
            chat_display.config(state=tk.DISABLED)
            chat_display.see(tk.END)
        except:
            print("Você foi desconectado do servidor!")
            client.close()
            break

def send_message():
    message = message_entry.get()
    client.send(message.encode("utf-8"))
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Você: {message}\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)
    message_entry.delete(0, tk.END)

def exit_chat():
    client.close()
    window.quit()

client.send(nickname.encode("utf-8"))

# Interface gráfica
window = tk.Tk()
window.title("Projeto Final - CHAT")
window.geometry("500x600")  # Define um tamanho inicial maior para melhor visibilidade

# Barra superior
header = tk.Frame(window, bg="blue violet", height=50)
header.pack(fill=tk.X)

title = tk.Label(header, text="Chatroom", bg="blue violet", fg="white", font=("Gabriola", 14, "bold"))
title.pack(side=tk.LEFT, padx=10, pady=5)

exit_button = tk.Button(header, text="Exit", command=exit_chat, bg="red", fg="white", font=("Helvetica", 12))
exit_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Área de exibição do chat
chat_frame = tk.Frame(window, bg="white")
chat_frame.pack(pady=(5, 0), padx=10, fill=tk.BOTH, expand=True)

chat_display = tk.Text(chat_frame, bg="white", font=("Helvetica", 12), wrap="word", state=tk.DISABLED)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Barra de rolagem
scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.config(yscrollcommand=scrollbar.set)

# Exibe uma mensagem de boas-vindas com instruções de uso
chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "Bem-vindo ao Chatroom!\nUse '@[nickname] [mensagem]' para enviar uma mensagem privada.\n\n")
chat_display.config(state=tk.DISABLED)

# Entrada de mensagem e botão de envio
bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

message_entry = tk.Entry(bottom_frame, font=("Helvetica", 12))
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

send_button = tk.Button(bottom_frame, text="Enviar", command=send_message, font=("Helvetica", 12), bg="green", fg="white")
send_button.pack(side=tk.RIGHT)

# Thread para receber mensagens
receive_thread = threading.Thread(target=receive)
receive_thread.start()

window.mainloop()
