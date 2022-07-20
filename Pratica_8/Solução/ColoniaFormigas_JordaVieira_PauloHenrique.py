import csv,pdb,math,random
import numpy as np

cidades = []

class Probabilidade:
	def __init__(self,cidade,chance):
		self.cidade = cidade
		self.chance = chance
	def __str__(self):
		return str(self.cidade) + "(" + str(self.chance) + "),"

class Cidade:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)
	def __str__(self):
		return "x=" + str(self.x) + ",y=" + str(self.y)

class Formiga:
	def __init__(self, cidadeInicial):
		self.cidade = cidadeInicial
		self.cidadeAtual = cidadeInicial
		self.solucaoParcial = [cidadeInicial]
		self.tamanhoRota = 0
		self.probabilidades = []

	def distancia(self, cidade1, cidade2):
		return math.sqrt((cidade2.x - cidade1.x)**2 + (cidade2.y - cidade1.y)**2)

	def escolherCidade(self):
		self.probabilidades = []
		somatorio = 0
		for i in range(0, len(cidades)):
			if(i not in self.solucaoParcial):
				somatorio += feromonio[self.cidade][i]**alfa * (1/(self.distancia(cidades[self.cidade],cidades[i]))**beta)

		for i in range(0, len(cidades)):
			if(i not in self.solucaoParcial):
				self.probabilidades.append(Probabilidade(i,(feromonio[self.cidade][i]**alfa * (1/(self.distancia(cidades[self.cidade],cidades[i]))**beta)/somatorio)))

		roleta = random.uniform(0,1)
		somatorio = 0
		for i in range(0, len(self.probabilidades)):
			somatorio += self.probabilidades[i].chance
			if(roleta < somatorio):	
				#print(len(self.probabilidades))
				#print(i)
				self.tamanhoRota += self.distancia(cidades[self.cidadeAtual],cidades[self.probabilidades[i].cidade])
				self.solucaoParcial.append(self.probabilidades[i].cidade)
				self.cidadeAtual = self.probabilidades[i].cidade
				return i

with open('Colonia.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	header = next(spamreader)
	for row in spamreader:
		x = row[0].split(';')[1].replace("['","").replace("']","")
		y = row[0].split(';')[2].replace("['","").replace("']","")
		cidades.append(Cidade(x,y))


maxIt = 1000
alfa = 1
beta = 1
menorCaminho = []
taxaEvaporacao = 0.4
Q = 1

feromonio = np.ones((len(cidades),len(cidades)))

menorRota = math.inf

for it in range(0, maxIt):
	# Criação das formigas
	formigas = []
	for i in range(0, len(cidades)):
		formigas.append(Formiga(i))

	print("Iteração: " + str(it))

	# Feromonio delta = 0
	feromonioD = np.zeros((len(cidades),len(cidades)))

	# Criar rota para cada formiga
	for c in range(0, len(cidades)):
		for formiga in formigas:
			formiga.escolherCidade()
	
	for formiga in formigas:
		if(formiga.tamanhoRota < menorRota):
			menorRota = formiga.tamanhoRota
			menorCaminho = formiga.solucaoParcial

	for formiga in formigas:
		for j in range(0,len(formiga.solucaoParcial)-1):
			feromonioD[formiga.solucaoParcial[j+1]][formiga.solucaoParcial[j]] += Q/formiga.tamanhoRota

	for i in range(0, len(cidades)):
		for j in range(0,len(cidades)):
			feromonio[i][j] = (1 - taxaEvaporacao)*feromonio[i][j] + feromonioD[i][j]
	print("Menor rota até agora: " + str(menorRota))
print("Menor rota: "+ str(menorRota))
print("Menor caminho: " + str(menorCaminho))

pdb.set_trace()