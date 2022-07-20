import sys, random
import numpy as np
import matplotlib.pyplot as plt

# Função sigmoidal
def sigmoid(x):
  return 1/(1+np.exp(-x))

# Função de ativação degrau
def funcAtivacaoDegrau(Y):
	for i in range(0, len(Y)):
		if(Y[i] >= 0):
			Y[i] = 1
		else:
			Y[i] = 0
	return Y

# Função de ativação sigmoidal
def funcAtivacaoSigmoide(Y):
	for i in range(0, len(Y)):
		Y[i] = sigmoid(Y[i])
	return Y

# Ajusta a saída do neurônio para classe de maior valor
def ajustaYiTesteSigmoide(Y):
	max_index = Y.index(max(Y))
	for i in range(0, len(Y)):
		Y[i] = 0

	Y[max_index] = 1
	return Y

# Calcula um novo bias dados bias atual, taxa de treino e erro
def calculaNovoBias(bias, taxaTreino, e):
	biasNovo = []
	for i in range(0, len(bias)):
			biasNovo.append(bias[i] + (taxaTreino * e[i]))
	return biasNovo

# Calcula novos pesos dados pesos atuais, taxa de treino, erro e amostra
def calculaNovoW(W, taxaTreino, e, X):
	Wnovo = W

	for i in range(0, len(X)):
		for j in range(0, len(e)):
			Wnovo[j][i] += (taxaTreino * e[j] * X[i])
	return Wnovo

# Calcula o erro da predição feita
def calculaE(yi, di):
	e = []
	for i in range(0, len(yi)):
		e.append(di[i] - yi[i])
	return e

# Calcula a saída do neurônio
def calculaYi(W, X, bias):
	Y = []
	WxB = []
	for i in range(0, len(W)):
		WxB.append(0)
	for i in range(0, len(W)):
		for j in range(0, len(X)):
			WxB[i] += W[i][j] * X[j]

	for i in range(0, len(WxB)):
		Y.append((WxB[i] + bias[i]))

	if(sys.argv[1] == 'deg'):
		Y = funcAtivacaoDegrau(Y)
	elif(sys.argv[1] == 'sig'):
		Y = funcAtivacaoSigmoide(Y)
	return Y
	
# Verificação do uso correto do parâmetro
try:
	if(sys.argv[1] != 'sig' and sys.argv[1] != 'deg'):
		print("Usar 'sig' ou 'deg' (sem aspas) como argumento para escolher a função de ativação.")
		sys.exit()
except IndexError:
	print("Usar 'sig' ou 'deg' (sem aspas) como argumento para escolher a função de ativação.")
	sys.exit()

#Leitura do arquivo
arquivoBD = open("column_3C.dat", "r")
linhasArquivoBD = arquivoBD.readlines()

amostras = []
amostrasTreino = []
amostrasTeste = []

classeNO = []
classeDH = []
classeSL = []

plotit = []
plote = []
plotacertos = []

# Adiciona todas as amostras em um array
for l in linhasArquivoBD:
	amostras.append(l.split(" "))

# Separa as amostras pelas classes
for amostra in amostras:
	if (amostra[6] == 'NO\n'):
		amostra.remove('NO\n')
		amostra.append(['1', '0', '0'])
		classeNO.append(amostra)

	elif (amostra[6] == 'DH\n'):
		amostra.remove('DH\n')
		amostra.append(['0', '1', '0'])
		classeDH.append(amostra)

	elif (amostra[6] == 'SL\n'):
		amostra.remove('SL\n')
		amostra.append(['0', '0', '1'])
		classeSL.append(amostra)

# Separa 2/3 de cada classe para treino e 1/3 para teste
for i in range(0, len(classeNO)):
	if(i <= len(classeNO) * 0.66):
		amostrasTreino.append(classeNO[i])
	else:
		amostrasTeste.append(classeNO[i])
for i in range(0, len(classeDH)):
	if(i <= len(classeDH) * 0.66):
		amostrasTreino.append(classeDH[i])
	else:
		amostrasTeste.append(classeDH[i])
for i in range(0, len(classeSL)):
	if(i <= len(classeSL) * 0.66):
		amostrasTreino.append(classeSL[i])
	else:
		amostrasTeste.append(classeSL[i])

# Embaralha as amostras de treino e teste
random.shuffle(amostrasTreino)
random.shuffle(amostrasTeste)

W = []
bias = []
maxit=15
taxaTreino = 0.1

# Inicializa W
for i in range(0,3):
	peso = []
	for j in range(0,6):
		peso.append(round(random.uniform(-1, 1), 2))
	W.append(peso)

# Inicializa bias
for i in range(0, 3):
	bias.append(round(random.uniform(-1, 1), 2))

E = 1
t = 1

while (t < maxit and E > 0):
	E = 0
	acertos = 0
	for amostra in amostrasTreino:
		X = list(map(float,amostra[:6]))
		di = list(map(int,amostra[6:][0]))
		yi = calculaYi(W, X, bias)
		e = calculaE(yi, di)
		W = calculaNovoW(W, taxaTreino, e, X)
		bias = calculaNovoBias(bias, taxaTreino, e)
		for i in range(0, len(e)):
			E += e[i] * e[i] 

	for amostra in amostrasTeste:
		X = list(map(float,amostra[:6]))
		di = list(map(int,amostra[6:][0]))
		yi = calculaYi(W, X, bias)
		if(sys.argv[1] == 'sig'):
			yi = ajustaYiTesteSigmoide(yi)
		e = calculaE(yi, di)
		if(e == [0,0,0]):
			acertos += 1
	plotit.append(t)
	plote.append(E)
	plotacertos.append(100*(acertos/len(amostrasTeste)))
	t += 1

# Exibe os pontos de erro geral e acertos por época
plt.plot(plotit, plote)
plt.plot(plotit, plotacertos)
plt.show()