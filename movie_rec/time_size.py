import pandas as pd
import time
from read_csv import df_rules

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

    def search(self, antecedents):
        node = self.root
        for char in antecedents:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.items

# Trie ağacını doldur
tree = TrieStruct()
for index, row in df_rules.iterrows():
    antecedent = row['antecedents']
    consequent = row['consequents']
    support = row['support']
    confidence = row['confidence']
    tree.insert(antecedent, consequent, support, confidence)

# Arama yapılacak değer
search_antecedents = "{1}"

# DataFrame arama süresi
start_time = time.time()
df_results = df_rules[df_rules["antecedents"] == search_antecedents]
df_search_time = time.time() - start_time
print("DataFrame arama süresi:", df_search_time, "saniye")

# Trie yapısında arama süresi
start_time = time.time()
trie_results = tree.search(search_antecedents)
trie_search_time = time.time() - start_time
print("Trie yapısı arama süresi:", trie_search_time, "saniye")

# Arama sonuçları
print("DataFrame sonuçları:", df_results)
print("Trie sonuçları:", trie_results)
