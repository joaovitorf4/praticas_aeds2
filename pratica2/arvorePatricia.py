import re

class Folha:
    def __init__(self, chave_bits, palavra_original, linha, coluna):
        self.chave_bits = chave_bits  # representação em inteiro (128 bits)
        self.palavra_original = palavra_original
        self.ocorrencias = [(linha, coluna)] # armazena todas as ocorrências (linha, coluna)

class NoInterno:
    def __init__(self, bit_indice, esquerdo, direito):
        self.bit_indice = bit_indice # o bit que este nó testa
        self.esquerdo = esquerdo
        self.direito = direito

class ArvorePatricia:
    def __init__(self):
        self.raiz = None

    def _get_bit(self, num, i):
        # retorna o i-ésimo bit de um número de 128 bits (da esquerda para a direita).
        # Como o máximo é 128 bits, o índice vai de 0 a 127
        return (num >> (127 - i)) & 1

    def _primeiro_bit_diferente(self, bits1, bits2):
        # encontra o índice do primeiro bit onde as duas chaves divergem.
        diff = bits1 ^ bits2
        if diff == 0:
            return None
        # encontra a posição do bit mais significativo que é 1
        return 127 - (diff.bit_length() - 1)

    def preparar_palavra(self, palavra):
        # converte palavra para 128 bits com preenchimento de brancos
        # trunca ou preenche com espaços até 16 caracteres
        palavra_pad = palavra.ljust(16, ' ')[:16]
        bits = 0
        for char in palavra_pad:
            bits = (bits << 8) | ord(char)
        return bits

    def inserir(self, palavra, linha, coluna):
        # implementa a lógica de inserção na Árvore Patrícia
        bits = self.preparar_palavra(palavra)

        # caso Árvore vazia
        if self.raiz is None:
            self.raiz = Folha(bits, palavra, linha, coluna)
            return

        # busca a folha que seria o destino natural para esta chave
        p = self.raiz
        while isinstance(p, NoInterno):
            if self._get_bit(bits, p.bit_indice) == 0:
                p = p.esquerdo
            else:
                p = p.direito

        # verifica se a palavra já existe (duplicata)
        if p.chave_bits == bits:
            p.ocorrencias.append((linha, coluna))
            return

        # encontra o primeiro bit diferente entre a nova chave e a folha encontrada
        bit_diff = self._primeiro_bit_diferente(bits, p.chave_bits)

        # reinicia a busca para inserir o novo NoInterno na posição correta do bit_diff
        self.raiz = self._inserir_na_posicao(self.raiz, bits, palavra, linha, coluna, bit_diff)

    def _inserir_na_posicao(self, no_atual, bits, palavra, linha, coluna, bit_diff):
        # se chegamos em uma folha ou em um nó interno cujo bit de teste > o bit_diff
        # devemos inserir o novo nó aqui.
        if isinstance(no_atual, Folha) or no_atual.bit_indice > bit_diff:
            novo_folha = Folha(bits, palavra, linha, coluna)
            
            # novo nó interno terá o bit_diff como índice de teste
            if self._get_bit(bits, bit_diff) == 0:
                return NoInterno(bit_diff, novo_folha, no_atual)
            else:
                return NoInterno(bit_diff, no_atual, novo_folha)

        # continua descendo na árvore até encontrar o ponto de inserção
        if self._get_bit(bits, no_atual.bit_indice) == 0:
            no_atual.esquerdo = self._inserir_na_posicao(no_atual.esquerdo, bits, palavra, linha, coluna, bit_diff)
        else:
            no_atual.direito = self._inserir_na_posicao(no_atual.direito, bits, palavra, linha, coluna, bit_diff)
        
        return no_atual
    
    def buscar(self, palavra):
        # implementação da busca ma árvore patrícia

        # se a árvore estiver vazia, não tem o que buscar
        if self.raiz is None: 
            return None
        
        # converte a arvore em 128 bits
        bits = self.preparar_palavra(palavra)
        no_atual = self.raiz

        # enquanto for nó interno, desce na árvore testando o bit correpondente
        while isinstance(no_atual, NoInterno):
            if self._get_bit(bits,no_atual.bit_indice) == 0:
                no_atual = no_atual.esquerdo
            else: 
                no_atual = no_atual.direito

        # quando chega na folha, verifica se não é um falso positivo, pois os nís internos não armazenam palavras
        if no_atual.chave_bits == bits:
            return no_atual.ocorrencias
        
        # se não bateu, a palavra não tá na árvore
        return None


def preenche_arvore(arvore, caminho_arquivo):
    # lê o arquivo de texto e insere cada palavra válida na Árvore Patrícia
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for num_linha, linha_texto in enumerate(arquivo, 1):
                # regex encontra sequências que começam com letra ([a-zA-Z])
                # seguidas por letras ou dígitos ([a-zA-Z0-9]*)
                for match in re.finditer(r'[a-zA-Z][a-zA-Z0-9]*', linha_texto):
                    palavra = match.group()
                    # correcao da coluna pra começar com 1
                    coluna = match.start() + 1
                    
                    # chama a inserção que criamos
                    arvore.inserir(palavra, num_linha, coluna)
                    
        print(f"Sucesso: o arquivo '{caminho_arquivo}' foi lido.")
    except FileNotFoundError:
        print(f"Erro: o arquivo '{caminho_arquivo}' não foi encontrado.")

# ÁREA DE EXECUÇÃO

if __name__ == "__main__":
    # cria Arvore Patricia para exemplo 1
    arvore1 = ArvorePatricia()

    # indexa arquivo exemplo 1
    preenche_arvore(arvore1, 'pratica2/exemplo1.txt')

    # palavras do exemplo 1
    palavras_busca_exemplo1 = ["trabalho", "computacao", "governo", "educacao", "tecnologia", "formacao", "desenvolvimento", "que", "informatica", "em", "crise"]

    # faz a impressão das palavras do exemplo 1
    print('\n' + "="*40)
    print("RESULTADOS DA BUSCA - EXEMPLO 1")
    print("="*40)

    for palavra in palavras_busca_exemplo1:
        ocorrencias = arvore1.buscar(palavra)
        if ocorrencias: 
            # imprime a linha e a coluna se a palavra foi encontrada ou avisa que não foi encontrada
            quantidade = len(ocorrencias)
            print(f"Palavra '{palavra}': ENCONTRADA ({quantidade} ocorrência(s)) -> Posições: {ocorrencias}")
        else: 
            print(f"Palavra '{palavra}': NÃO ENCONTRADA")
            
    # cria Arvore Patricia para exemplo 2
    arvore2 = ArvorePatricia()

    # indexa arquivo exemplo 2
    preenche_arvore(arvore2, 'pratica2/exemplo2.txt')

    # palavras do exemplo 2
    palavras_busca_exemplo2 = ["sociedade", "software", "ideia", "pessoa", "Informatica", "etica", "muito", "ciencia", "computacao", "que", "area", "moral"]

    # faz a impressão das palavras do exemplo 2
    print('\n' + "="*40)
    print("RESULTADOS DA BUSCA - EXEMPLO 2")
    print("="*40)

    for palavra in palavras_busca_exemplo2:
        ocorrencias = arvore2.buscar(palavra)
        if ocorrencias: 
            # imprime a linha e a coluna se a palavra foi encontrada ou avisa que não foi encontrada
            quantidade = len(ocorrencias)
            print(f"Palavra '{palavra}': ENCONTRADA ({quantidade} ocorrência(s)) -> Posições: {ocorrencias}")
        else: 
            print(f"Palavra '{palavra}': NÃO ENCONTRADA")