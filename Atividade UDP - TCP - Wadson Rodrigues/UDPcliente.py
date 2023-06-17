import socket

class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def enviar_resposta(self, numero_questao, numero_alternativas, respostas):
        mensagem = f"{numero_questao};{numero_alternativas};{respostas}"
        self.socket.sendto(mensagem.encode(), (self.host, self.port))

        data, addr = self.socket.recvfrom(1024)
        resposta = data.decode()
        partes = resposta.split(';')

        numero_questao = int(partes[0])
        acertos = int(partes[1])
        erros = int(partes[2])

        print(f"Resposta para a questão {numero_questao}: acertos={acertos} erros={erros}")

cliente = Cliente('127.0.0.1', 1234)
cliente.enviar_resposta(1, 5, 'VVFFV')
cliente.enviar_resposta(2, 4, 'VVVV')

