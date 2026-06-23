import itertools
import random
import time
import matplotlib.pyplot as plt

def gerar_matriz_distancias(n):
    """Gera uma matriz n x n com distâncias aleatórias positivas."""
    matriz = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distancia = random.randint(1, 100)
                matriz[i][j] = distancia
                matriz[j][i] = distancia 
    return matriz

def caixeiro_viajante_forca_bruta(matriz):
    """Resolve o TSP testando todas as permutações possíveis (força bruta)."""
    n = len(matriz)
    cidades_restantes = list(range(1, n)) 
    menor_distancia = float('inf')

    for permutacao in itertools.permutations(cidades_restantes):
        distancia_atual = 0
        cidade_atual = 0 

        for proxima_cidade in permutacao:
            distancia_atual += matriz[cidade_atual][proxima_cidade]
            cidade_atual = proxima_cidade

        distancia_atual += matriz[cidade_atual][0]

        if distancia_atual < menor_distancia:
            menor_distancia = distancia_atual

    return menor_distancia

# ==========================================
# Execução e Geração do Gráfico (Relatório)
# ==========================================

n_maximo = 14 # Recomendo testar até 13. Para n=14 o tempo de espera será longo.

# Listas para guardar os dados e colocar no gráfico depois
tamanhos_n = []
tempos_execucao = []

print(f"{'Tamanho (n)':<15} | {'Tempo (segundos)':<15}")
print("-" * 35)

for n in range(2, n_maximo + 1):
    matriz = gerar_matriz_distancias(n)
    
    inicio = time.perf_counter()
    caixeiro_viajante_forca_bruta(matriz)
    fim = time.perf_counter()
    
    tempo_gasto = fim - inicio
    
    # Armazena as informações de n e tempo
    tamanhos_n.append(n)
    tempos_execucao.append(tempo_gasto)
    
    print(f"{n:<15} | {tempo_gasto:.6f}")

# ==========================================
# Geração do Gráfico (Matplotlib)
# ==========================================

plt.figure(figsize=(8, 6))

# Plota a linha conectando os pontos (n, tempo)
plt.plot(tamanhos_n, tempos_execucao, marker='o', color='red', linestyle='-', linewidth=2)

# Adiciona títulos e rótulos aos eixos
plt.title('Crescimento Exponencial do Tempo - Força Bruta (TSP)', fontsize=14, pad=15)
plt.xlabel('Tamanho do Problema (Número de Cidades - n)', fontsize=12)
plt.ylabel('Tempo de Execução (Segundos)', fontsize=12)

# Adiciona uma grade ao fundo e força a exibição dos números inteiros no eixo x
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(tamanhos_n)

plt.tight_layout()

# Salva a imagem automaticamente na mesma pasta do script
plt.savefig('crescimento_forca_bruta_tsp.png', dpi=300)

# Exibe o gráfico na tela
plt.show()