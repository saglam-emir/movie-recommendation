from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from matrix import user_movie_matrix


# apriori algoritmasını kullanarak birliktelik kurallarını çıkarmaya başlıyoruz

# sık film kümelerini bulma
frequent_itemsets = apriori(user_movie_matrix,min_support=0.29,use_colnames=True)
print("Sık kullanılan öğe kümeleri:\n", frequent_itemsets)

#birliktelik kurallarını çıkarma 
rules = association_rules(frequent_itemsets,metric="confidence",min_threshold=0.02)
rules.to_csv("association_rules.csv", index=False)
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])


