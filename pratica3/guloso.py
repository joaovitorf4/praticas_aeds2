import heapq
import random
import matplotlib.pyplot as plt
import os

# variavel global que define o limite maximo de vertices para o teste de grafos completos
LIMITE_N = 1000

# funcao de leitura dos arquivos (mantido da sua logica original)
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

                # garante que origem e destino existam no grafo
                if u not in grafo:
                    grafo[u] = []
                if v not in grafo:
                    grafo[v] = []

                grafo[u].append((v, peso))
    return grafo

# funcao da Heuristica Gulosa
def heuristica_gulosa(grafo, origem):
    # inicializa as distancias de todos os vertices com infinito
    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[origem] = 0
    visitados = set()

    # fila de prioridade armazena tuplas (peso_da_aresta, vizinho, vertice_anterior)
    fila_prioridade = [(0, origem, origem)]

    comparacoes = 0

    while fila_prioridade:
        peso_atual, vertice_atual, vertice_anterior = heapq.heappop(fila_prioridade)

        # primeira comparacao: verifica se o vértice ja foi visitado e o caminho e obsoleto
        comparacoes += 1
        if vertice_atual in visitados:
            continue

        visitados.add(vertice_atual)

        # atualiza a distancia total baseada na escolha gulosa que foi feita
        if vertice_atual != origem:
            distancias[vertice_atual] = distancias[vertice_anterior] + peso_atual

        for vizinho, peso_aresta in grafo[vertice_atual]:
            # segunda comparacao: evita adicionar a fila vertices que ja foram consolidados
            comparacoes += 1
            if vizinho not in visitados:
                heapq.heappush(fila_prioridade, (peso_aresta, vizinho, vertice_atual))

    return distancias, comparacoes

# funcao que junta os vertices para formar o grafo completo (Mantido)
def gerar_grafo_completo(num_vertices):
    grafo = {i: [] for i in range(1, num_vertices + 1)}
    for i in range(1, num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                peso = random.randint(1, 100)
                grafo[i].append((j, peso))
    return grafo

# faz os testes para responder as questoes (a) a (e)
def executar_testes_e_plotar_guloso():
    print("Iniciando testes com grafos completos (Algoritmo Guloso)...")

    n_sucesso = []
    comparacoes_realizadas = []

    for n in range(4, LIMITE_N + 1):
        try:
            print(f"Tentando alocar e testar grafo com N = {n}...")
            grafo = gerar_grafo_completo(n)
            _, comparacoes = heuristica_gulosa(grafo, 1)

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
        plt.plot(n_sucesso, comparacoes_realizadas, marker='o', linestyle='-', color='r')
        plt.title('Heurística Gulosa: Número de Vértices vs Comparações')
        plt.xlabel('Número de Vértices (N)')
        plt.ylabel('Número de Comparações')
        plt.grid(True)
        print("Feche a janela do gráfico para continuar a execução dos testes em instâncias reais.")
        plt.show()

# faz os testes para responder a questao (f)
def executar_instancias_dimacs_guloso():
    print("\nIniciando testes nas instâncias DIMACS com Algoritmo Guloso...")
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

        if not grafo:
            print(f"O grafo em {arquivo} está vazio ou inválido.")
            continue

        ultimo_vertice = max(grafo.keys())

        # executa o algoritmo com origem no vertice 1
        distancias, comparacoes = heuristica_gulosa(grafo, 1)
        distancia_final = distancias.get(ultimo_vertice, float('inf'))

        print(f"--- Resultados (Guloso) para {arquivo} ---")
        print(f"  Distância encontrada do vértice 1 ao vértice {ultimo_vertice}: {distancia_final}")
        print(f"  Número de comparações realizadas: {comparacoes}")
        print("-" * 40)


if __name__ == '__main__':
    # executa as questoes de (a) a (e) para o Guloso
    executar_testes_e_plotar_guloso()

    # executa a questao (f) para o Guloso
    executar_instancias_dimacs_guloso()