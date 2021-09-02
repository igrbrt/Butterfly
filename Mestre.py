#!/usr/bin/python
# encoding: utf-8
# python version: 3.3
# filename: Mestre.py
# author: igor

import socket
import math

class Mestre:
    listaEscravos = []
    numeroEscravos = idConectados = 0
    porta = 1110
    inicio = fim = fatia = 0
    numeroProcessar = somatorio = somaPar = ids = 0
    servidor = None
    udp = None
    
    
    def inicializar(self):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor = ('localhost', self.porta)
        self.udp.bind(self.servidor)
    
    def fechar(self):
        self.udp.close()
    
    def esperaEscravos(self):
        i = 1;
        while i <= int(self.numeroEscravos):
            msg, enderecoCliente = self.udp.recvfrom(1111)
            print ('Cliente ', i ,' conectado !')
            #insere na lista o ID e o Endereco do Escravo
            self.listaEscravos.insert(i,enderecoCliente)
            self.udp.sendto (bytes(str(i).encode('utf-8')), enderecoCliente)
            self.udp.sendto (bytes(str(self.numeroEscravos).encode('utf-8')), enderecoCliente)
            
            self.porta = self.porta + 1
            tempDados = "%s-%s-%s-%s\n" % (i,enderecoCliente[0], self.porta, self.porta+1)
            self.porta = self.porta + 1
            
            file = open('listaId','a')
            file.write(str(tempDados))
            file.close()
            i = i + 1
    
    def buscaId(self,ids):
        file = open('listaId','r')
        linha = ''
        aux = None
        for linha in file.readlines():
            line = linha.split('-')
            if int(line[0]) == ids:
                aux = line
        return aux
    
    def calculafatias(self):
        self.fatia = int( self.numeroProcessar/self.numeroEscravos )
        self.inicio = (self.fatia * self.ids)
        self.fim = (self.fatia * (self.ids + 1))
        
    def processa(self):
        i = self.inicio
        while i < self.fim+1:
            self.somatorio += i
            i = i + 1

if __name__ == '__main__':
    
    mestre = Mestre()
    mestre.inicializar()
    
    print ('\n\t\t==================================\n')
    print ('\t\t\tButterfly - Servidor\n')
    
    print ('Digite o numero de escravos - multiplo de dois: ')
    mestre.numeroEscravos = int(input())
    
    while int(mestre.numeroProcessar) < int(mestre.numeroEscravos):
        print ('\nNumero para processar: ')
        mestre.numeroProcessar = int(input())
    
    file = open('listaId', 'w')
    
    tempDados = "%s-%s-%s-%s\n" % (mestre.ids, 'localhost', mestre.porta, mestre.porta + 1)
    file.write(str(tempDados))
    file.close()
    
    mestre.porta = mestre.porta + 1
    
    print ('\nAguardando clientes...')
    
    mestre.esperaEscravos()
    
    qtdMensagens = int(math.log(mestre.numeroEscravos))
    i=0
    while i < mestre.numeroEscravos:
        mestre.udp.sendto (bytes(str(mestre.numeroProcessar).encode('utf-8')), mestre.listaEscravos[i])
        i = i + 1
    
    mestre.calculafatias()
    mestre.processa()
    i=0
    receberID = int(mestre.numeroEscravos/2)
    while i < qtdMensagens+1:
        receber = mestre.buscaId(mestre.ids)
        somaAux, fim = mestre.udp.recvfrom(1024)
        somaAux = int(somaAux.decode('utf-8'))
        mestre.somatorio += somaAux
        receberID = int(receberID/2)
        i = i+1
    
    print('\n\n\t\t >> Resultado: ', mestre.somatorio)
    
    mestre.fechar()
        
        
