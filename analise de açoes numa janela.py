import yfinance as yf
import PySimpleGUI as sg
import matplotlib.pyplot as plt


# funções
def br_code(msg):
    """
    Concatena o codigo da ação com o sulfixo ".SA" (requerimento do yfinance).
    :param msg: Codigo da ação nacional a ser analizada.
    :return: Retorna o codigo da ação pronto para ser usado
    """
    new_code = (msg+'.SA').upper()
    return new_code


# tema da janela
sg.theme('Darkgreen6')

# cada "[]" representa uma linha e cada valor (separado por virgulas dento do "[]") representa uma coluna
layout = [
    [sg.Text('digite o codigo da ação'), sg.Input(key='ticket', size=(41, 1))],
    [sg.Text('O que deseja analisar?'), sg.Checkbox('Valor (R$)', key='valor'),
     sg.Checkbox('Dividendos (R$)', key='divid'), sg.Checkbox('Grafico', key='grafico')],
    [sg.Button('Mostrar analise', key='analise')],
    [sg.Text('', key='valor_ticket')],
    [sg.Text('', key='dividendos')],
    [sg.Text('', key='informa')],
    [sg.Text('Historico de Analise:')],
    [sg.Output(size=(60, 7))]
]

# comando que inicia a janela com o nome e disposição da janela (layout)
janela = sg.Window('SUPER ANALISE DO SUPER LEOZAO', layout)

# dentro de um looping infinito se nao qualquer interação com a janela ira encerra-la
while True:
    eventos, valores = janela.read()  # eventos sao os cliques com mouse, valores sao informaçoes digitadas nos campos
    if eventos == sg.WINDOW_CLOSED:  # faz o "x" funcionar para encerrar o programa (famoso "alt+f4")
        break

    if eventos == 'analise':  # se a caixa Analise estiver ticada ele lê o bloco
        t = br_code(valores['ticket'].upper())
        stock = yf.Ticker(t)
        if valores['valor']:
            janela['valor_ticket'].update('O valor da ação é de R${:.2f}'.format(stock.history('max')['Close'][-1]))

        stock = stock.history('max')['Dividends']
        ticker_year_dividend = (stock[stock.index > '2021-01-01']).sum()

        if valores['divid']:  # se a caixa dividendos estiver ticada ele lê o bloco
            janela['dividendos'].update('Esse ano foi distribuido R${:.2f}'.format(ticker_year_dividend))

        stock = yf.Ticker(t)
        stock = stock.info
        janela['informa'].update(stock['longBusinessSummary'][:24])
        print('Analise: {}'.format(valores['ticket']))

        if valores['grafico']:  # se a caixa grafico estiver ticada ele lê o bloco
            stock = yf.Ticker(t)
            plt.plot(stock.history('max')['Close'], )
            plt.show()

janela.close()
