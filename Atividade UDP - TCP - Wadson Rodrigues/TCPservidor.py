import threading
import socket

class Estatistica:
    def __init__(self):
        self.questoes = {}

    def atualizar_estatistica(self, questao, acertos, erros):
        if questao in self.questoes:
            self.questoes[questao]['acertos'] += acertos
            self.questoes[questao]['erros'] += erros
        else:
            self.questoes[questao] = {'acertos': acertos, 'erros': erros}

    def obter_estatistica(self):
        return self.questoes

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.estatistica = Estatistica()

    def iniciar(self):
        self.socket.bind((self.host, self.port))
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            data, addr = self.socket.recvfrom(1024)
            thread = threading.Thread(target=self.processar_requisicao, args=(data, addr))
            thread.start()

    def processar_requisicao(self, data, addr):
        mensagem = data.decode()
        partes = mensagem.split(';')

        numero_questao = int(partes[0])
        numero_alternativas = int(partes[1])
        respostas = partes[2]

        # Realize aqui a lógica de correção das respostas

        # Exemplo simples: contar V (verdadeiro) como acerto e F (falso) como erro
        acertos = respostas.count('V')
        erros = respostas.count('F')

        self.estatistica.atualizar_estatistica(numero_questao, acertos, erros)

        resposta = f"{numero_questao};{acertos};{erros}".encode()
        socket_envio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_envio.sendto(resposta, addr)
        socket_envio.close()

        print(f"Recebida resposta da questão {numero_questao} de {addr[0]}:{addr[1]}")

servidor = Servidor('127.0.0.1', 1234)
servidor.iniciar()
