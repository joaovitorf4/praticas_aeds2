import time

def ler_arquivo_tsp(caminho_arquivo):
    dimensao = 0
    formato_peso = ""
    valores_arestas = []
    lendo_pesos = False

    # Abre o arquivo e realiza a leitura linha por linha para extrair cabeçalho e dados
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha == "EOF":
                break

            if "DIMENSION" in linha:
                dimensao = int(linha.split(":")[-1].strip())
                continue

            if "EDGE_WEIGHT_FORMAT" in linha:
                formato_peso = linha.split(":")[-1].strip()
                continue

            if "EDGE_WEIGHT_SECTION" in linha:
                lendo_pesos = True
                continue

            if lendo_pesos:
                try:
                    valores_arestas.extend(map(int, linha.split()))
                except ValueError:
                    break

    # Inicializa a matriz quadrada preenchida com zeros
    matriz = [[0] * dimensao for _ in range(dimensao)]
    idx = 0

    # Reconstrói a matriz simétrica caso o formato seja diagonal superior
    if formato_peso == "UPPER_DIAG_ROW":
        for i in range(dimensao):
            for j in range(i, dimensao):
                matriz[i][j] = valores_arestas[idx]
                matriz[j][i] = valores_arestas[idx]
                idx += 1

    # Reconstrói a matriz simétrica caso o formato seja diagonal inferior
    elif formato_peso == "LOWER_DIAG_ROW":
        for i in range(dimensao):
            for j in range(i + 1):
                matriz[i][j] = valores_arestas[idx]
                matriz[j][i] = valores_arestas[idx]
                idx += 1

    return matriz, dimensao


def aproximado_mst(matriz, dimensao):
    if dimensao == 0:
        return [], 0

    # Encontra a Árvore Geradora Mínima (MST) usando o Algoritmo de Prim
    chave = [float('inf')] * dimensao
    pai = [-1] * dimensao
    na_mst = [False] * dimensao

    chave[0] = 0

    for _ in range(dimensao - 1):
        # Encontra o vértice com a menor chave que ainda não está na MST
        min_chave = float('inf')
        u = -1
        for v in range(dimensao):
            if not na_mst[v] and chave[v] < min_chave:
                min_chave = chave[v]
                u = v

        na_mst[u] = True

        # Atualiza a chave e o pai dos vértices adjacentes
        for v in range(dimensao):
            if matriz[u][v] > 0 and not na_mst[v] and matriz[u][v] < chave[v]:
                pai[v] = u
                chave[v] = matriz[u][v]

    # Constrói a lista de adjacência da MST para facilitar a DFS
    arvore = [[] for _ in range(dimensao)]
    for i in range(1, dimensao):
        if pai[i] != -1:
            arvore[pai[i]].append(i)
            arvore[i].append(pai[i])

    # Faz a travessia em pré-ordem (DFS) na MST usando pilha
    visitado = [False] * dimensao
    rota = []
    pilha = [0] 

    while pilha:
        u = pilha.pop()
        if not visitado[u]:
            visitado[u] = True
            rota.append(u)
            # Insere os vizinhos na pilha na ordem inversa
            for v in reversed(arvore[u]):
                if not visitado[v]:
                    pilha.append(v)

    # Calcula a distância total do caminho no grafo original
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += matriz[rota[i]][rota[i+1]]
    
    # Fecha o ciclo (volta à cidade inicial)
    distancia_total += matriz[rota[-1]][rota[0]]
    rota.append(rota[0])

    return rota, distancia_total

# Gera o relatorio dos dados encontrados 
def relatorio_aproximado(arquivos_tsp):
    resultados = []

    for arquivo in arquivos_tsp:
        try:
            matriz, dimensao = ler_arquivo_tsp(arquivo)

            tempo_inicio = time.time()
            rota, distancia = aproximado_mst(matriz, dimensao)
            tempo_fim = time.time()

            tempo_execucao = tempo_fim - tempo_inicio

            print(f"--- Instância: {arquivo} ---")
            print(f"Dimensão: {dimensao} cidades")
            print(f"Distância (Algoritmo Aproximado - MST): {distancia}")
            print(f"Tempo de Execução: {tempo_execucao:.6f} segundos\n")

            resultados.append((arquivo, distancia, tempo_execucao))

        except FileNotFoundError:
            print(f"Erro: O arquivo '{arquivo}' não foi encontrado.\n")

    return resultados


if __name__ == "__main__":
    arquivos = ['si535.tsp', 'pa561.tsp', 'si1032.tsp']
    resultados_aprox = relatorio_aproximado(arquivos)