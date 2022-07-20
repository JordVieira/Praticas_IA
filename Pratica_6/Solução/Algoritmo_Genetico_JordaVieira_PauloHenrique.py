import random, math
import matplotlib.pyplot as plt

# Retorna o valor da função objetivo dados x1 e x2
def calcFObjetivo(x1,x2):
	return (math.sqrt(x1) * math.sin(x1)) * (math.sqrt(x2) * math.sin(x2))

# Gera mutação em genes do indivíduo baseado em uma taxa
def gerarMutacao(individuo):
	for i in range(0,2):
		sorteioMutacao = random.uniform(0,1)
		if(sorteioMutacao <= taxaMutacao):
			individuo[i] *= random.uniform(0.9,1.1)
	return individuo

# Gera um filho cruzando genes dos pais
def gerarFilho(pai1,pai2):
	filho = []

	fatorEscalonamento = random.uniform(0,1)

	x1 = fatorEscalonamento * pai1[0] + (1 - fatorEscalonamento) * pai2[0]
	x2 = fatorEscalonamento * pai1[1] + (1 - fatorEscalonamento) * pai2[1]

	filho.append(x1)
	filho.append(x2)
	filho = gerarMutacao(filho)
	fObjetivo = calcFObjetivo(filho[0],filho[1])
	filho.append(fObjetivo)
	filho.append(0)

	return filho

# Calcula os valores da função objetivo (melhor, pior, médio) de toda a população
def calcResultados(populacao):
	soma = 0
	plotpior.append(populacao[99][2])
	plotmelhor.append(populacao[0][2])
	for i in range(0, len(populacao)):
		soma += populacao[i][2]
	plotmedio.append(soma/len(populacao))

# Parâmetros do algoritmo genético
rankingLinearMin = 1
rankingLinearMax = 100
taxaCruzamento = 0.7
taxaMutacao = 0.1
maxIt = 20

populacao = []
plotit = []
plotpior = []
plotmelhor = []
plotmedio = []

# Geração de genes aleatórios e criação da primeira população
for i in range(0,100):
	individuo = []

	x1 = round(random.uniform(0,10), 2)
	x2 = round(random.uniform(0,10), 2)

	fObjetivo = calcFObjetivo(x1,x2)

	individuo.append(x1)
	individuo.append(x2)
	individuo.append(fObjetivo)
	individuo.append(0)

	populacao.append(individuo)
	
# Um loop para evoluir a população com base em uma iteração máxima
for it in range(0, maxIt):
	print('iteração ' + str(it+1))

	# A população é ordenada conforme o valor objetivo
	populacao.sort(key=lambda x: x[2], reverse=True)

	calcResultados(populacao)	
	print('melhor: ' + str(populacao[0][2]))
	print('pior: ' + str(populacao[99][2]))
	
	# Criação da fita baseado nas aptidões de cada indivíduo
	tamanhoFita = 0
	fita = []
	for i in range(0, len(populacao)):
		aptidaoIndividuo = round(rankingLinearMin + (rankingLinearMax - rankingLinearMin) * ((len(populacao)-(i+1))/(len(populacao)-1)),0)
		populacao[i][3] = aptidaoIndividuo	
		tamanhoFita += aptidaoIndividuo

	# Seleção aleatória de 100 indivíduos para cruzamento
	selecionadosCruzamento = []
	for i in range(0,100):
		sorteio = random.uniform(0,tamanhoFita)
		somatorioAptidao = 0
		for j in range(0,100):
			somatorioAptidao += populacao[j][3]
			if(sorteio <= somatorioAptidao):
				selecionadosCruzamento.append(populacao[j])
				break
			somatorioAptidao += populacao[j][3]

	# Criação da nova população fazendo cruzamento entre pares de indivíduos
	novaPopulacao = []
	for i in range(0,100,2):
		sorteioCruzamento = random.uniform(0,1)
		if(sorteioCruzamento <= taxaCruzamento):
			filho1 = gerarFilho(selecionadosCruzamento[i],selecionadosCruzamento[i+1])
			filho2 = gerarFilho(selecionadosCruzamento[i],selecionadosCruzamento[i+1])

			novaPopulacao.append(filho1)
			novaPopulacao.append(filho2)
		else: # Se os pais não se cruzam, podem ser mutados e passar para a nova geração
			pai1 = gerarMutacao(selecionadosCruzamento[i])
			pai2 = gerarMutacao(selecionadosCruzamento[i+1])

			pai1[2] = calcFObjetivo(pai1[0],pai1[1])
			pai2[2] = calcFObjetivo(pai2[0],pai2[1])

			novaPopulacao.append(pai1)
			novaPopulacao.append(pai2)
	populacao = novaPopulacao
	plotit.append(it)
	print('\n')

# Printa um gráfico com a evolução do melhor, pior e resultado médio a cada iteração (ou geração)
plt.plot(plotit, plotpior)
plt.plot(plotit, plotmelhor)
plt.plot(plotit, plotmedio)
plt.show()