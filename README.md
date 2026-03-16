# Práticas de Algoritmos e Estruturas de Dados II (AEDs 2)

Este repositório contém as atividades práticas desenvolvidas para a disciplina de **Algoritmos e Estruturas de Dados II** no **CEFET-MG (Departamento de Computação)**.

O objetivo é a implementação, análise de performance e comparação de diferentes estruturas de dados e algoritmos de busca e ordenação.

---

## 📂 Práticas Realizadas

### [Prática 01] - Árvore Binária de Pesquisa (ABP) vs. Árvore AVL
Comparação de desempenho e eficiência entre uma Árvore Binária de Pesquisa sem balanceamento e uma Árvore AVL.

* **Objetivo:** Analisar o custo computacional (número de comparações) em operações de busca.
* **Implementações Realizadas:**
  * Métodos de **Inserção** e **Busca** para Árvore Binária de Pesquisa Sem Balanceamento (elementos inteiros).
  * Métodos de **Inserção** e **Busca** para Árvore AVL (elementos inteiros).
* **Metodologia de Experimento:**
  * Geração de 10 árvores a partir de $n$ elementos **ordenados** (n de 10.000 a 100.000, com intervalo de 10.000).
  * Geração de 10 árvores a partir de $n$ elementos **aleatórios** (n de 10.000 a 100.000, com intervalo de 10.000).
  * Busca pelo elemento fixo `100.001` em cada árvore gerada para contabilizar o número de comparações.
* **Entregáveis:**
  * Código-fonte comentado.
  * Gráficos de $n \times \text{número de comparações}$ para inserções ordenadas.
  * Tabelas comparativas com os resultados encontrados.

---

## 🛠️ Configuração do Projeto

* **Linguagem:** (Ex: C / C++ / Java / Python)
* **Compilador/Interpretador:** (Ex: GCC 11.4 / Python 3.10)

---

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/joaovitorf4/praticas_aeds2.git
   cd praticas_aeds2
   ```

2. **Execução:**
   * Execute os códigos de acordo com as linguagens utilizadas em cada prática.
