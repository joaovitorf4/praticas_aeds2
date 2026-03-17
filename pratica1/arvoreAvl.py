import random

class NoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.esquerdo = None
        self.direito = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def buscar(self, noAtual, valorBuscado, quantidade = 0): # Busca um valor na árvore AVL recursivamente
        if noAtual is None:
            return (False, quantidade)

        if valorBuscado < noAtual.valor:
            return self.buscar(noAtual.esquerdo, valorBuscado, quantidade+1)

        elif valorBuscado > noAtual.valor:
            return self.buscar(noAtual.direito, valorBuscado, quantidade+1)

        else:
            return (True, quantidade)

    def getAltura(self, no): # Retorna a altura de um nó
        if no is None:
            return 0

        return no.altura     

    def getFatorBalanceamento(self, no): # Calcula o fator de rebalanceamento de um nó
        if no is None: 
            return 0

        return self.getAltura(no.esquerdo) - self.getAltura(no.direito)

    def rsd(self, y): # Realiza uma rotação siples à direita
        x = y.esquerdo
        subArvoreDir = x.direito
        x.direito = y
        y.esquerdo = subArvoreDir
        y.altura = 1 + max(self.getAltura(y.direito), self.getAltura(y.esquerdo))
        x.altura = 1 + max(self.getAltura(x.direito), self.getAltura(x.esquerdo))
        return x
    
    def rse(self, y): # Realiza uma rotação simpels à esquerda
        x = y.direito
        subArvoreEsq = x.esquerdo
        x.esquerdo = y
        y.direito = subArvoreEsq
        y.altura = 1 + max(self.getAltura(y.direito), self.getAltura(y.esquerdo))
        x.altura = 1 + max(self.getAltura(x.direito), self.getAltura(x.esquerdo))
        return x
    
    def rde(self, no): # Realiza uma rotação dupla: direita-esquerda
        no.direito = self.rsd(no.direito)
        no = self.rse(no)
        return no
    
    def rdd(self, no): # Realiza uma rotação dupla: esquerda-direita
        no.esquerdo = self.rse(no.esquerdo)
        no = self.rsd(no)
        return no
    
    def inserir(self, noAtual, valor): # Insere um valor na árvore AVL mantendo o balanceamente
        if noAtual is None:
            return NoAVL(valor)
        
        if valor < noAtual.valor:
            noAtual.esquerdo = self.inserir(noAtual.esquerdo, valor)

        elif valor > noAtual.valor:
            noAtual.direito = self.inserir(noAtual.direito, valor)
        
        noAtual.altura = 1 + max(self.getAltura(noAtual.direito), self.getAltura(noAtual.esquerdo))

        fb = self.getFatorBalanceamento(noAtual)

        if fb > 1:
            if valor < noAtual.esquerdo.valor:
                return self.rsd(noAtual)
            
            elif valor > noAtual.esquerdo.valor:
                return self.rdd(noAtual)
            
        elif fb < -1:
            if valor > noAtual.direito.valor:
                return self.rse(noAtual)
            
            elif valor < noAtual.direito.valor:
                return self.rde(noAtual)

        return noAtual        
    
# ÁREA DE EXECUÇÃO

if __name__ == "__main__":
    tamanhos = []
    comps_ordenadas = []
    comps_aleatorias = []

    print("--- Experimentos da Árvore AVL ---")
    
    print("\n- TESTE 1: INSERÇÕES ORDENADAS\n")
    for i in range(1, 11):
        n = i * 10000
        arvore = ArvoreAVL()

        for i in range(1, n + 1):
            arvore.raiz = arvore.inserir(arvore.raiz, i)

        achou, comparacoes = arvore.buscar(arvore.raiz, 100001)
        comps_ordenadas.append(comparacoes)

        print(f"Árvore com {n} elementos ordenados:")
        print(f" Nùmero de comparações realizadas: {comparacoes}")
        print("-" * 40)

    print("\n- TESTE 2: INSERÇÕES ALEATÓRIAS\n")
    for i in range(1, 11):
        n = i * 10000
        tamanhos.append(n)
        arvore = ArvoreAVL()

        elementos = list(range(1, n+1))
        random.shuffle(elementos)

        for i in elementos:
            arvore.raiz = arvore.inserir(arvore.raiz, i)

        achou, comparacoes = arvore.buscar(arvore.raiz, 100001)
        comps_aleatorias.append(comparacoes)

        print(f"Árvore com {n} elementos aleatórios:")
        print(f" Número de comparações realizadas: {comparacoes}")
        print("-" * 40)