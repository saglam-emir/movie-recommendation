import sys
import pandas as pd
from read_csv import df_rules


# DataFrame bellek kullanımı
dataframe_size = sys.getsizeof(df_rules)
print("DataFrame bellek kullanımı:", dataframe_size, "bayt")

# Trie yapısı
class TrieNode:
    def __init__(self):
        self.children = {}
        self.items = []

class TrieStruct:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, antecedents, consequents, support, confidence):
        node = self.root
        for char in antecedents:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.items.append((consequents, support, confidence))

# Trie ağacını doldur
tree = TrieStruct()
for index, row in df_rules.iterrows():
    antecedent = row['antecedents']
    consequent = row['consequents']
    support = row['support']
    confidence = row['confidence']
    tree.insert(antecedent, consequent, support, confidence)

# Trie yapısının bellek kullanımı
trie_size = sys.getsizeof(tree) + sum(sys.getsizeof(node) for node in tree.root.children.values())
print("TrieStruct bellek kullanımı:", trie_size, "bayt")
