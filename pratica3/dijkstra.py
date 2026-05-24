import heapq
import random
import matplotlib.pyplot as plt
import os

# Variável global que define o limite máximo de vértices para o teste de grafos completos
LIMITE_N = 1000

# Metodo de leitura dos arquivos
def ler_grafo_dimacs(caminho_arquivo):
    grafo = {}
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.split()
            if not partes:
                continue

            if partes[0] == 'a':
                u = int(partes[1])
                v = int(partes[2])
                peso = int(partes[3])

                # Garante que origem e destino existam no grafo
                if u not in grafo:
                    grafo[u] = []
                if v not in grafo:
                    grafo[v] = []

                grafo[u].append((v, peso))
    return grafo

# Metodo do algoritmo de dijkstra
def dijkstra(grafo, origem):
    # Inicializa as distâncias de todos os vértices com infinito
    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[origem] = 0

    # Fila de prioridade armazena tuplas (distancia, vertice)
    fila_prioridade = [(0, origem)]

    comparacoes = 0

    while fila_prioridade:
        distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)

        # Primeira comparação: verifica se o caminho atual é obsoleto
        comparacoes += 1
        if distancia_atual > distancias[vertice_atual]:
            continue

        for vizinho, peso in grafo[vertice_atual]:
            distancia_calculada = distancia_atual + peso

            # Segunda comparação: processo de relaxamento da aresta
            comparacoes += 1
            if distancia_calculada < distancias.get(vizinho, float('inf')):
                distancias[vizinho] = distancia_calculada
                heapq.heappush(fila_prioridade, (distancia_calculada, vizinho))

    return distancias, comparacoes

# Metodo que junta os vertices para formar o grafo completo
def gerar_grafo_completo(num_vertices):
    grafo = {i: [] for i in range(1, num_vertices + 1)}
    for i in range(1, num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                peso = random.randint(1, 100)
                grafo[i].append((j, peso))
    return grafo

# Faz os testes para responder as questões (a) a (e)
def executar_testes_e_plotar():
    print("Iniciando testes com grafos completos...")

    n_sucesso = []
    comparacoes_realizadas = []

    # Laço alterado para variar de 1 em 1 até o limite de 1.000.000
    for n in range(4, LIMITE_N + 1):
        try:
            print(f"Tentando alocar e testar grafo com N = {n}...")
            grafo = gerar_grafo_completo(n)
            _, comparacoes = dijkstra(grafo, 1)

            n_sucesso.append(n)
            comparacoes_realizadas.append(comparacoes)
            print(f"Sucesso: {comparacoes} comparações.")

            del grafo

        except MemoryError:
            print(f"Limite de memória atingido em N = {n}. Encerrando a geração de grafos completos.")
            break
        except Exception as e:
            print(f"Erro inesperado em N = {n}: {e}")
            break

    if n_sucesso:
        plt.figure(figsize=(10, 6))
        plt.plot(n_sucesso, comparacoes_realizadas, marker='o', linestyle='-', color='b')
        plt.title('Dijkstra: Número de Vértices vs Comparações')
        plt.xlabel('Número de Vértices (N)')
        plt.ylabel('Número de Comparações')
        plt.grid(True)
        print("Feche a janela do gráfico para continuar a execução dos testes em instâncias reais.")
        plt.show()

# Faz os testes para responder a questão (f)
def executar_instancias_dimacs():
    print("\nIniciando testes nas instâncias DIMACS...")
    arquivos = [
        "NY Dist.txt",
        "NY time.txt",
        "San Francisco Dist.txt",
        "San Francisco Time.txt"
    ]

    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            print(f"Arquivo não encontrado: {arquivo} (ignorando)")
            continue

        print(f"Carregando e processando {arquivo}...")
        grafo = ler_grafo_dimacs(arquivo)

        # Define o último vértice baseado no maior ID numérico extraído do dicionário
        if not grafo:
            print(f"O grafo em {arquivo} está vazio ou inválido.")
            continue

        ultimo_vertice = max(grafo.keys())

        # Executa o algoritmo com origem no vértice 1
        distancias, comparacoes = dijkstra(grafo, 1)
        distancia_final = distancias.get(ultimo_vertice, float('inf'))

        print(f"--- Resultados para {arquivo} ---")
        print(f"  Distância mínima do vértice 1 ao vértice {ultimo_vertice}: {distancia_final}")
        print(f"  Número de comparações realizadas: {comparacoes}")
        print("-" * 40)


if __name__ == '__main__':
    # Executa as questões de (a) a (e)
    executar_testes_e_plotar()

    # Executa a questão (f)
    executar_instancias_dimacs()