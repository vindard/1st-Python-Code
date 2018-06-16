import random
n = 15

# Note algorithm is not a robust sort
# It only works if initial order is assumed as presented below
rankings = [
["Einstein", "Feynmann"],
["Feynmann", "Gell-Mann"],
["Gell-Mann", "Thorne"],
["Einstein", "Lorentz"],
["Lorentz", 'Planck'],
["Hilbert", "Noether"],
["Poincare", "Noether"]
]

# Flatten data
source_with_dups = [name for pair in rankings for name in pair]
source = []
for name in source_with_dups:
    if name not in source:
        source.append(name)

# Assign result-instance counts for multiple rounds with shuffled inputs
source_count = {}
for name in source:
    source_count[name] = {}
    for i in range(len(source)):
        source_count[name][i] = 0

# Shuffles the order of pairs 'n' times for testing
for i in range(n):
    uniques = source
    random.shuffle(rankings)
    
    # This bubble-sorts the list
    for pair in rankings:
        if uniques.index(pair[0]) > uniques.index(pair[1]):
            uniques.insert(uniques.index(pair[1]),uniques.pop(uniques.index(pair[0])))    
    
    # This counts the result-instances and stores in 'source_count'
    for j, name in enumerate(uniques):
        source_count[name][j] += 1
    
    #Uncomment below line to see inside loop (n times)
    #print(f"\n\nRandom Order Round {i+1}\nRanking shuffled: {rankings}\n\nUnique set after: {uniques}")


# Checks whether input rankings-data is good
list_integrity = True
final_result = {}
for key in source_count:
    v = list(source_count[key].values())
    k = list(source_count[key].keys())
    final_result[key] = k[v.index(max(v))]
    if list_integrity == False:
        False
    else:
        list_integrity =  n == v[v.index(max(v))]

ordered_result = sorted(final_result.items(), key = lambda x: x[1])

print(f"List data is good: {list_integrity} on {n} tries\n")
print('\n'.join(map(str, ordered_result)))