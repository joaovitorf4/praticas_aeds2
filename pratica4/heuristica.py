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


import time


def vizinho_mais_proximo(matriz, dimensao, cidade_inicial=0):
    # Inicializa o controle de cidades visitadas e define o ponto de partida da rota
    visitados = [False] * dimensao
    rota = [cidade_inicial]
    visitados[cidade_inicial] = True
    distancia_total = 0
    cidade_atual = cidade_inicial

    # Busca iterativamente a cidade não visitada mais próxima da localização atual
    for _ in range(dimensao - 1):
        proxima_cidade = None
        menor_distancia = float('inf')

        for vizinho in range(dimensao):
            if not visitados[vizinho] and cidade_atual != vizinho:
                distancia = matriz[cidade_atual][vizinho]
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    proxima_cidade = vizinho
        # Registra a cidade selecionada na rota e acumula a distância percorrida
        rota.append(proxima_cidade)
        visitados[proxima_cidade] = True
        distancia_total += menor_distancia
        cidade_atual = proxima_cidade

    # Soma a distância de retorno à cidade de origem para fechar o ciclo
    distancia_total += matriz[cidade_atual][cidade_inicial]
    rota.append(cidade_inicial)

    return rota, distancia_total

# Gera o relatorio dos dados encontrados usando a heuristica de vizinho mais proximo
def relatorio_heuristica(arquivos_tsp):
    resultados = []

    for arquivo in arquivos_tsp:
        try:
            matriz, dimensao = ler_arquivo_tsp(arquivo)

            tempo_inicio = time.time()
            rota, distancia = vizinho_mais_proximo(matriz, dimensao)
            tempo_fim = time.time()

            tempo_execucao = tempo_fim - tempo_inicio

            print(f"--- Instância: {arquivo} ---")
            print(f"Dimensão: {dimensao} cidades")
            print(f"Distância Mínima (Heurística Vizinho Mais Próximo): {distancia}")
            print(f"Tempo de Execução: {tempo_execucao:.6f} segundos\n")

            resultados.append((arquivo, distancia, tempo_execucao))

        except FileNotFoundError:
            print(f"Erro: O arquivo '{arquivo}' não foi encontrado.\n")

    return resultados


if __name__ == "__main__":
    arquivos = ['si535.tsp', 'pa561.tsp', 'si1032.tsp']
    resultados = relatorio_heuristica(arquivos)