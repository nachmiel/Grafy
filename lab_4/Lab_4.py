import os

os.system('cls' if os.name == 'nt' else 'clear')

with open("lab_4\graf.txt", "r") as file:
    lines = file.read().splitlines()

first_line = lines[0]
first_value = int(first_line.split()[0]) #liczba wierzchołków
second_value = int(first_line.split()[1]) #liczba krawędzi

# print(f"Stopnie wierzchołków:")
# w = 0
# sequence = []
# for x in range(1,first_value+1):
#     w += 1
#     numb = 0
#     for char in lines[1:]: 
#         v1 = int(char.split(" ")[0])
#         v2 = int(char.split(" ")[1])
#         if x == v1 or x == v2:
#             numb += 1
#     sequence.append(numb)
#     print(f"deg({w})={numb}")
# print(f"Ciag stopni grafu G: {sorted(sequence)}")

lista_Sasiedztwa = []
for i in range(1, first_value + 1):
    lista_Sasiedztwa.append([])

print(lista_Sasiedztwa)

for x in range(1,first_value+1):
    for char in lines[1:]:
        vi = int(char.split(" ")[0])
        vj = int(char.split(" ")[1])
        wk = int(char.split(" ")[2])
        lista_Sasiedztwa[vi].append(f"{vj} {wk}") #https://zpe.gov.pl/a/przeczytaj/DPNBGJ0t8 algorytmu Dijkstry

print(lista_Sasiedztwa) # [[], ['2 28', '4 15', '2 28', '4 15', '2 28', '4 15', '2 28', '4 15'], ['3 37', '4 42', '3 37', '4 42', '3 37', '4 42', '3 37', '4 42'], ['4 95', '4 95', '4 95', '4 95'], []]
