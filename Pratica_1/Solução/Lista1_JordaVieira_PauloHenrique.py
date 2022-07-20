# Busca A*
# Jordã Vieira Macena, Paulo Henrique da Costa Silva

import math

# Uma classe para guardar as distâncias até cidades vizinhas, 
# o valor da heurística e se ela já foi expandida
class Cidade:
    def __init__(self, nome, cidadesVizinhas):
        self.nome = nome
        self.cidadesVizinhas = cidadesVizinhas
        self.distanciaBucareste = 0
        self.expandida = False
    
    # Atualiza a borda expandindo a cidade e colocando os custos com heurística
    def expandir(self, borda, custoCaminhoAtual, cidadeAtual):
        print('\nExpandindo ' + self.nome)
        # Cada cidade vizinha é inserida na borda com as cidades antecessoras e seus respectivos custos
        for key in self.cidadesVizinhas: 
            novoNo = borda[cidadeAtual].cidades.copy()
            novoNo[key] = int(custoCaminhoAtual) + listaCidades[cidadeAtual].cidadesVizinhas[key]
            borda[key] = Caminho(novoNo, int(custoCaminhoAtual) + listaCidades[cidadeAtual].cidadesVizinhas[key] + int(listaCidades[key].distanciaBucareste))

        self.expandida = True
        return None

# Uma classe para guardar as cidades que compõem um dado caminho e seu custo total
class Caminho:
    def __init__(self, cidades, custo):
        self.cidades = cidades
        self.custo = custo

# Uma classe para guardar o ponto de partida da busca, a cidade e custo atual, 
# e a borda com os possíveis caminhos
class Busca:
    def __init__(self, origem):
        self.origem = origem
        self.cidadeAtual = origem
        self.custoCaminhoAtual = 0 #
        self.borda = {origem : Caminho({origem:0},0)} # Inicialmente a borda contém a origem
    
    # Expande a cidade atual atualizando a borda, e define a próxima cidade a ser expandida
    # baseado nos custos com heurística
    def expandir(self):
    
        listaCidades[self.cidadeAtual].expandir(self.borda, self.custoCaminhoAtual, self.cidadeAtual) 
        
        custo = math.inf
        custoProx = math.inf
        prox = None

        # Procura o menor custo dentre os existentes na borda, e define a próxima expansão
        for key in self.borda:
            if(listaCidades[key].expandida is False):
                print(key + '=' + str(self.borda[key].custo) + ', ', end='')
            if(self.borda[key].custo < custo and listaCidades[key].expandida is False):
                prox = key
                custo = self.borda[key].custo
                
        print("\n")
        custoProx = custo - int(listaCidades[prox].distanciaBucareste)

        # A expansão continua caso a próxima cidade não seja Bucareste
        if(prox is not None and prox != 'Bucareste'):
            self.custoCaminhoAtual = custoProx
            self.cidadeAtual = prox

            self.expandir()
        
    # Mostra o menor caminho calculado, as cidades que o compõem
    # e os custos entre uma e outra, além do custo total
    def mostrar(self):
        print("\nMenor Caminho:")
        cidadesLista = [*self.borda['Bucareste'].cidades]
        cidadesCusto = self.borda['Bucareste'].cidades

        for i in range(0, len(cidadesLista) - 1):
            print(cidadesLista[i] + " -> " + str(cidadesCusto[cidadesLista[i+1]] - cidadesCusto[cidadesLista[i]]) + " -> " + cidadesLista[i+1])
        print("\nCusto Total = " + str(cidadesCusto['Bucareste']))
        
# Leitura dos arquivos
arquivoGrafo = open("Grafo.txt", "r")
arquivoHeuristica = open("Heuristica.txt", "r")
linhasGrafo = arquivoGrafo.readlines()
linhasHeuristica = arquivoHeuristica.readlines()

listaCidades = {}

# Preenchimento das heurísticas de cada cidade
for l in linhasHeuristica:
    nome = l.split(';')[0]
    distanciaBucareste = l.split(';')[1].replace('\n','')
    cidade = Cidade(nome,{})
    cidade.distanciaBucareste = distanciaBucareste
    listaCidades[l.split(';')[0]] = cidade

# Preenchimento das distâncias entre cidades
for l in linhasGrafo:
    cidadeA = l.split(';')[0]
    cidadeB = l.split(';')[1]
    distanciaAB = int(l.split(';')[2])

    if cidadeA not in listaCidades[cidadeB].cidadesVizinhas:
        listaCidades[cidadeA].cidadesVizinhas[cidadeB] = distanciaAB
        listaCidades[cidadeB].cidadesVizinhas[cidadeA] = distanciaAB
    if cidadeB not in listaCidades[cidadeA].cidadesVizinhas:
        listaCidades[cidadeB].cidadesVizinhas[cidadeA] = distanciaAB
        listaCidades[cidadeA].cidadesVizinhas[cidadeB] = distanciaAB

# Definindo a busca pelo menor caminho a partir de um ponto inicial
busca = Busca("Arad")
busca.expandir()
busca.mostrar()

