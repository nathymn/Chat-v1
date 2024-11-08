import threading
import socket

host = "127.0.0.1"
port = 3308

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criando uma Socket
server.bind((host, port)) #Associando Socket a uma porta e servidor
server.listen() #Coloca o servidor para escutar conexões (0)

clients = {}
nicknames = {}

def broadcast(message, sender=None):
    for nickname, client in clients.items():
        if client != sender:  # Não enviar de volta para o remetente
            client.send(message.encode("utf-8"))

def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode("utf-8") #O número 1024 especifica o número máximo de bytes que o servidor espera receber de uma vez.
            
            if message.startswith("@"):
                # Unicast message
                target_nickname = message.split(" ")[0][1:]
                if target_nickname in clients:
                    target_client = clients[target_nickname]
                    target_client.send(f"{nickname} (privado): {' '.join(message.split(' ')[1:])}".encode("utf-8"))
                else:
                    client.send(f"{target_nickname} não está conectado.".encode("utf-8"))
            else:
                # Broadcast message para todos, exceto o remetente
                broadcast(f"{nickname}: {message}", sender=client)
        except:
            # Remover cliente em caso de erro
            address = client.getpeername()  # Obter IP e porta do cliente
            client.close()
            del clients[nickname]
            broadcast(f"{nickname} saiu do chat.")
            print(f"{nickname} (IP: {address[0]}, Porta: {address[1]}) saiu do chat")
            break

def receive():
    while True:
        client, address = server.accept()
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        clients[nickname] = client

        print(f"{nickname} entrou com IP: {address[0]}, Porta: {address[1]}")
        broadcast(f"{nickname} entrou no chat!")

        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

print("Servidor está funcionando e rodando...")
receive()
