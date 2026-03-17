# Árvore Binária de Pesquisa sem Balanceamento

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class UnbalancedBST:
    def __init__(self):
        self.root = None

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

