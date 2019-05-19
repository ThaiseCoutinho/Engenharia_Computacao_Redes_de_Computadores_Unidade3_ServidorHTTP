# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
# ALUNO: THAISE MARIA COUTINHO DE LIMA
# ALUNO: BRUNA REGO DE MOURA
#
# SCRIPT: Base de um servidor HTTP
#
# 
# importacao das bibliotecas
import socket
import os 
import datetime
# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print 'Servidor HTTP aguardando conexoes na porta %s ...' % PORT
i = 0 #A cada solicitacao que acontece implemento o i.
while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    conectado = True #Essa variavel controla o estado da conexao, sumponde que a mesma eh pesistente incialmente.
    while conectado: #Enquanto estiver conectado.
        try: #Permite que tente enquanto a conexao persistente esta ativa. O metodo .recv recebe os dados enviados por um cliente atraves do socket, ou seja le requisicao.
    	    request = client_connection.recv(1024)
           # imprime na tela o que o cliente enviou ao servidor
            print request
            lista = request.split() #split divide a string em uma lista, onde cada palavra eh um item da lista.
	    if len(lista) > 4: #Testa se a requisicao eh valida, ou seja, se tem dados suficiente.
		
                comando = lista[0] #Pega o comando
		caminho = lista[1] #Pega o caminho
		versao = lista[2] #Pega versao do protocolo
		conexao = lista[4] #Pega o tipo de conexao
		
		if caminho == "/":
		    caminho = "index.html"		
		
		if comando == 'GET':
		    cabecalho = "HTTP/1.1 200 OK\r\n\r\n"
		    caminho = caminho[1:]#retira '/' do caminho a ser lido
		    try:
		        arquivo = open(caminho,'r')
		    except IOError:
		        cabecalho = "HTTP/1.1 404 Not Found\r\n\r\n"		
		        arquivo = open('notFound.html','r')
		    http_response = cabecalho + arquivo.read() #reposta para o comando GET
		    arquivo.close()
		 
		else: #Para comando diferente do comando GET
		    cabecalho = "HTTP/1.1 400 Bad Request\r\n\r\n"
		    arquivo = open('badRequest.html','r')
		    http_response = cabecalho + arquivo.read()
		    arquivo.close()


  		if conexao == "keep-alive":#se pedido de conexao persistente: seta timeout
                    client_connection.settimeout(20) #Para fazer apenas uma requisicao e manter o canal aberto por um determinado tempo
                else:#se nao sai do laco e encerra conexao
                    conectado = False
                    
            client_connection.send(http_response) #Envia resposta pra o cliente
            
        except: #Expirou o tempo do timeout
            conectado = False #Sai do laco
            
    client_connection.close() #Encerra conexao
    print "conexao do cliente [ %s ] encerrada" %i
    print "###########################################################################"
    i+=1
# encerra o socket do servidor
listen_socket.close()
