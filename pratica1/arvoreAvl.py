class NoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.esquerdo = None
        self.direito = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def buscar(self, noAtual, valorBuscado):
        if noAtual is None:
            return False

        if valorBuscado < noAtual.valor:
            return self.buscar(noAtual.esquerdo, valorBuscado)

        elif valorBuscado > noAtual.valor:
            return self.buscar(noAtual.direito, valorBuscado)

        else:
            return True

