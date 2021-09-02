#!/usr/bin/python
# encoding: utf-8
# python version: 3.3
# filename: Escravo.py
# author: igor

import socket

class Escravo:
    servidor = None
    udp = None
    porta = 1110
    destino = idMestre = meuId = None
    inicio = fim = fatia = soma = somatorio = 0
    
    def inicializar(self):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.porta = 1110 + 2 * self.getNumeroEscravos()
        self.udp.bind(('localhost',int(self.porta)))

    def fechar(self):
        self.udp.close()

    def getNumeroEscravos(self):
        file = open('listaId','r')
        cont = 0
        for linha in file.readlines():
            cont += 1
        return cont

    def encontraMetade(self,ids):
        file = open('listaId','r')
        linhas = ''
        mestre = None
        for linhas in file.readlines():
            line = linhas.split('-')
            if int(line[0]) == ids:
                mestre = line
        return mestre
    
    def processa(self):
        i = self.inicio
        while i < self.fim+1:
            self.soma += i
            i = i + 1

if __name__ == '__main__':
    escravo = Escravo()
    escravo.idMestre = escravo.encontraMetade(0)
    escravo.inicializar()

    print ('\n\t\t==================================\n')
    print ('\t\t\tButterfly - Escravo\n')
    print ('\n\nPronto para processar !\n')
    
    escravo.destino = (escravo.idMestre[1],int(escravo.idMestre[2]))
    msg = 'Conectado!'
    escravo.udp.sendto(bytes(msg.encode('utf-8')), escravo.destino)
    
    escravo.meuId, endereco = escravo.udp.recvfrom(escravo.porta+1)
    escravo.meuId = int(escravo.meuId.decode('utf-8'))
    
    print('ID: ', escravo.meuId)
    
    qtdEscravos, endereco = escravo.udp.recvfrom(escravo.porta+1)
    qtdEscravos = int(qtdEscravos.decode('utf-8'))
    
    numero, endereco = escravo.udp.recvfrom(escravo.porta+1)
    numero = int(numero.decode('utf-8'))
    
    escravo.fatia = int(numero/qtdEscravos)
    escravo.inicio = (escravo.fatia * escravo.meuId) + 1
    escravo.fim = escravo.fatia * (escravo.meuId+1)
    
    if escravo.meuId == qtdEscravos-1:
        escravo.fim += numero % qtdEscravos
    
    print('\nProcessando...')
    
    escravo.processa()
    
    metade = qtdEscravos
    
    while True:
        metade = int(metade/2)
        escravo.somatorio = escravo.soma
        
        if escravo.meuId >= metade:
            enviarParaId = int(escravo.meuId - metade)
            escravo.idMestre = escravo.encontraMetade(enviarParaId)
            
            print('Enviando soma parcial para: ', enviarParaId)
            
            escravo.destino = (escravo.idMestre[1],int(escravo.idMestre[2]))
            escravo.udp.sendto(bytes(str(escravo.soma).encode('utf-8')), escravo.destino)
            
            print('\nEnviado !')
        
        elif escravo.meuId > 0:
            receberDeId = int(escravo.meuId + metade)
            escravo.idMestre = escravo.encontraMetade(escravo.meuId)
            
            print('\nAguardando soma parcial de: ', receberDeId)
            
            escravo.soma, endereco = escravo.udp.recvfrom(escravo.porta+1)
            escravo.soma = int(escravo.soma.decode('utf-8'))
            
            print('\nRecebido !')
            
            escravo.somatorio += escravo.soma
            escravo.soma = escravo.somatorio
        
        if not (escravo.meuId < metade):
            escravo.fechar()
            break

    
    
