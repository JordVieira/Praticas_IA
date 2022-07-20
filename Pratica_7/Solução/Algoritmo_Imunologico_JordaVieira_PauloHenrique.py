import pdb
import random
import math 
import matplotlib.pyplot as plt
import numpy as np

maxIt = 50
n1 = 50
N = n1
n2 = 0
beta = 0.1
nc = beta * n1
ro = 5

def transp(m):
	return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def func(X,Y):
    arr = []
    for x in X:
        line = []
        for y in Y:
            line.append(math.sqrt(x) * math.sin(x)*math.sqrt(y) * math.sin(y))
        arr.append(line)
    return arr

def plot_geracao_3d(populacao, iteracao):
	fig = plt.figure(figsize= (16,9))
	ax = plt.axes(projection = '3d')

	X = np.linspace(0,10,40)
	Y = np.linspace(0,10,40)
	Z = func(X,Y)
	X,Y = np.meshgrid(X,Y)

	ax.contour3D(X, Y, Z, 40, cmap='binary', alpha = 0.2)
	        
	ax.grid(b = True, color = 'grey', linestyle = '-.', linewidth = 0.3, alpha = 0.2)

	my_cmap = plt.get_cmap('hsv')

	sctt = ax.scatter3D(transp(populacao)[0],transp(populacao)[1], transp(populacao)[2], alpha = 0.8, c=transp(populacao)[2], cmap= my_cmap, marker = '.')

	plt.title(f"Funcao alpine2 - iteracao {iteracao}")
	ax.set_xlabel('x1')
	ax.set_ylabel('x2')
	ax.set_zlabel('f(x1,x2)')
	fig.colorbar(sctt, ax=ax, shrink= 0.5, aspect = 5)

	plt.show()
	plt.clf()
	plt.close()

def plotar(populacao, t):
	plt.rcParams['figure.figsize'] = (16,19)
	plt.style.use('seaborn-bright')
	fig = plt.figure(figsize= (16,9))
	ax = plt.axes()
	plt.title(f"Funcao alpine2 - Geracao {t}")
	X = np.linspace(0,10,40)
	Y = np.linspace(0,10,40)
	Z = func(X,Y)
	X,Y = np.meshgrid(X,Y)

	plt.contour(X, Y, Z)

	ax.grid(b = True, color = 'grey', linestyle = '-.', linewidth = 0.3, alpha = 0.2)

	my_cmap = plt.get_cmap('hsv')

	#pdb.set_trace()

	sctt = ax.scatter(transp(populacao)[0],transp(populacao)[1], transp(populacao)[2], alpha = 1, linewidth = 6, c=transp(populacao)[2], cmap= my_cmap, marker = '.')

	ax.set_xlabel('x1')
	ax.set_ylabel('x2')
	fig.colorbar(sctt, ax=ax, shrink= 0.5, aspect = 5)
	fig.set_size_inches(18.5, 10.5)
	plt.show()
	plt.clf()
	plt.close()

def calcFObjetivo(x1,x2):
	return (math.sqrt(x1) * math.sin(x1)) * (math.sqrt(x2) * math.sin(x2))

def mutacao(C, txMutacao):
	Cmutado = C[:]
	for i in range(0,2):
		rd = random.uniform(0,1)
		#pdb.set_trace()
		if(rd < txMutacao):
			Cmutado[i] *= random.uniform(0.9,1.1)
			#Cmutado[i] = random.uniform(0,10)
	return Cmutado

P = []

for i in range(0,100):
	anticorpo = []

	x1 = round(random.uniform(0,10), 2)
	x2 = round(random.uniform(0,10), 2)

	fObjetivo = calcFObjetivo(x1,x2)

	anticorpo.append(x1)
	anticorpo.append(x2)
	anticorpo.append(fObjetivo)
	anticorpo.append(i+1)

	P.append(anticorpo)

for it in range(0, maxIt):

	P.sort(key=lambda x: x[2], reverse=True)
	for i in range(0,len(P)):
		P[i][3] = i+1

	#pdb.set_trace()

	if(it % 10 == 0):
		plot_geracao_3d(P, it)
		plotar(P, it)

	# Seleção
	P1 = []
	for i in range(0, n1):
		P1.append(P[i])
	# Clonagem
	C = []
	for i in range(0, n1):
		Nc = (beta * N)
		for j in range(0, int(Nc)):
			C.append(P[i])	
	# Mutação
	C1 = []
	for i in range(0, len(C)):
		Da = (i+1)/(n1)
		txMutacao = 1 - np.exp(-ro * Da)
		C1.append(mutacao(C[i],txMutacao))

	# Eval
	for i in range(0,len(C1)):
		C1[i][2] = calcFObjetivo(C1[i][0],C1[i][1])

	P2 = []
	for i in range(0,len(C1),5):
		maior = i
		for j in range(0,5):
			if(C1[i+j][2] > C1[i+0][2]):
				maior = i + j
		P2.append(C1[maior])

	P2.sort(key=lambda x: x[2], reverse=True)

	#pdb.set_trace()
	P = P2

plot_geracao_3d(P, 50)
plotar(P, 50)
#pdb.set_trace()