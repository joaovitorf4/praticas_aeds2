# Árvore Binária de Pesquisa sem Balanceamento
import random
import math
import matplotlib.pyplot as plt

# Classe de Nó que sera usado na arvore binaria para armazenar a posição de cada elemento
class Node:
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None

# Classe da arvore binaria não ordenada
class UnbalancedBST:
	def __init__(self):
		self.root = None

	# Insere o elemento na arvore fazendo as comparações maior e menor necessarias
	def insert(self, key):
		if self.root is None:
			self.root = Node(key)
			return

		current = self.root
		while True:
			if key == current.key:
				break

			if key < current.key:
				if current.left is None:
					current.left = Node(key)
					break
				current = current.left
			else:
				if current.right is None:
					current.right = Node(key)
					break
				current = current.right

	# A função busca um elemento na arvore e retorna o numero de comprações e se encontrou
	def search_with_comparisons(self, key):
		comparisons = 0
		current = self.root

		while current is not None:
			comparisons += 1
			if key == current.key:
				return True, comparisons
			elif key < current.key:
				current = current.left
			else:
				current = current.right
		return False, comparisons

if __name__ == "__main__":
	# Elemento de pesquisa fora do range para testar o pior caso de busca em todos os cenários
	elemento_pesquisa = 100001

	tamanhos = []
	comps_aleatorias = []
	comps_ordenadas = []

	# Gerar 10 arvores de n elementos aleatórios variando de 10000 a 100000 elementos indo de 10000 em 10000
	for i in range(1, 11):
		n = i * 10000
		tamanhos.append(n)
		arvore_aleatoria = UnbalancedBST()

		# Criando lista e embaralhando para garantir inserção aleatória
		elementos = list(range(1, n + 1))
		random.shuffle(elementos)

		for valor in elementos:
			arvore_aleatoria.insert(valor)

		encontrado, num_comparacoes = arvore_aleatoria.search_with_comparisons(elemento_pesquisa)
		comps_aleatorias.append(num_comparacoes)

		print(f"Árvore com {n} elementos aleatórios:")
		print(f"  Número de comparações realizadas: {num_comparacoes}")
		print("-" * 40)

	# Gerar 10 arvores de n elementos ordenados variando de 10000 a 100000 elementos indo de 10000 em 10000
	for i in range(1, 11):
		n = i * 10000
		arvore = UnbalancedBST()

		# Inserindo n elementos de forma ordenada
		for valor in range(1, n + 1):
			arvore.insert(valor)

		encontrado, num_comparacoes = arvore.search_with_comparisons(elemento_pesquisa)
		comps_ordenadas.append(num_comparacoes)

		print(f"Árvore com {n} elementos ordenados:")
		print(f"  Número de comparações realizadas: {num_comparacoes}")
		print("-" * 40)

    # Gera o grafico com os dados coletados a cima
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, comps_aleatorias, marker='o', label='Aleatórios')
    plt.plot(tamanhos, comps_ordenadas, marker='s', label='Ordenados')
    plt.title('Comparação do Número de Comparações na Busca')
    plt.xlabel('Quantidade de Elementos (n)')
    plt.ylabel('Número de Comparações')
    plt.legend()
    plt.grid(True)

    # Salva o gráfico em um arquivo de imagem no mesmo diretório
    plt.savefig("grafico.png")

    plt.show()