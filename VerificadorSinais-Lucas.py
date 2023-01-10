from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta, date
from colorama import init, Fore, Back
from time import time
import sys

init(autoreset=True)

print(Fore.YELLOW+
"""
###################################
#------VERIFICADOR DE SINAIS------#
#--------- LUCAS ARAUJO ----------#
###################################
"""
)

print('-> Versão - 2.3.0 - Free'+Fore.RESET+'\n')


API = IQ_Option('your email', 'your password')
API.connect()

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()

timeframe = 1


while True:
    input('\nVERIFICAR ARQUIVO SINAIS.TXT? APERTE ENTER PARA CONFIRMAR.')
    arquivo = open('sinais.txt', 'r').read()
    arquivo = arquivo.split('\n')

    gales = -1
    print('\nQuantos gales? (0-3)', end='')
    while gales < 0 or gales > 3:
        gales = int(input())

    print('\nLista de outro dia?')
    data_lista = input(' -> informe a data da lista (YYYY-MM-DD) ou ENTER se for de hoje:')

    win = 0
    wingale = [0 , 0,  0]
    loss = 0

    if data_lista == '':
        data_lista = datetime.now().strftime('%Y-%m-%d')
    print(data_lista)
    print('\n')

    for dados in arquivo:
        if dados == '':
            continue
        dados = dados.split(';')
        
        timeframe = int(dados[0].replace("M", ""))

        
        
        hora = datetime.strptime(data_lista+' '+dados[2], '%Y-%m-%d %H:%M:%S')
        
        hora = hora + timedelta(0, int(gales)*(timeframe*60))
        hora = datetime.timestamp(hora)

        velas = API.get_candles(dados[1].upper(), (timeframe*60), (gales+1), int(hora) )

        if int(velas[-1]['from']) == int(hora):
            

            perdeu = True
            for i in range(gales+1):
                dir = 'call' if velas[i]['open'] <  velas[i]['close'] else 'put' if velas[i]['open'] >  velas[i]['close'] else 'doji'
                if dir == dados[3].lower():
                    if i == 0:
                        print(dados[0]+';'+dados[1]+';'+dados[2]+';'+dados[3]+('' if dados[3] == 'CALL' else ' ')+' - '+Fore.GREEN+'Win  \u2705')
                    else:
                        print(dados[0]+';'+dados[1]+';'+dados[2]+';'+dados[3]+('' if dados[3] == 'CALL' else ' ')+' - '+Fore.GREEN+'Win'+str(i)+' \u2705'+str(i*'\U0001f413'))
                        wingale[i-1] += 1 
                        
                    win += 1
                    perdeu = False
                    break
            
            if perdeu:        
                print(dados[0]+';'+dados[1]+';'+dados[2]+';'+dados[3]+('' if dados[3] == 'CALL' else ' ')+' - '+Fore.RED+'Loss \u274c')
                loss +=1
        else:
            print(dados[0]+';'+dados[1]+';'+dados[2]+';'+dados[3]+('' if dados[3] == 'CALL' else ' ')+' - '+Fore.RED+'?')


    print(50 * '-')
    print('[RESULTADOS]')
    print('Wins: '+Fore.GREEN+str(win))
    for i in range(gales):
        print('Wins com gale '+str(i+1)+':'+Fore.GREEN+str(wingale[i]))
    print('Loss: '+Fore.RED+str(loss))

    if (gales > 0):
        perdareal = loss * (3 ** gales)
        print('Proporção real de Ganho X Perda *: '+str(win)+' x '+str(perdareal))
        print(' * Considerando valor do gale = x2')

    if input('APERTE [enter] PARA SAIR ou [n] PARA TESTAR NOVA LISTA') != 'n':
        sys.exit()
