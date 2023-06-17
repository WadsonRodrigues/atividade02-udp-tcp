import socket

class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def enviar_respostas_arquivo(self, arquivo):
        socket_envio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        with open(arquivo, 'r') as file:
            for linha in file:
                partes = linha.strip().split(';')

                numero_questao = int(partes[0])
                numero_alternativas = int(partes[1])
                respostas = partes[2]

                mensagem = f"{numero_questao};{numero_alternativas};{respostas}"
                socket_envio.sendto(mensagem.encode(), (self.host, self.port))

                data, addr = socket_envio.recvfrom(1024)
                resposta = data.decode()
                partes_resposta = resposta.split(';')

                numero_questao_resposta = int(partes_resposta[0])
                acertos = int(partes_resposta[1])
                erros = int(partes_resposta[2])

                print(f"Resposta para a questão {numero_questao_resposta}: acertos={acertos} erros={erros}")

        socket_envio.close()

cliente = Cliente('127.0.0.1', 1234)
cliente.enviar_respostas_arquivo('respostas.txt')