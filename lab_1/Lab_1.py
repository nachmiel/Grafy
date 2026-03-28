import re 
import numpy as np
import os

os.system('cls' if os.name == 'nt' else 'clear')


file_name = input("Podaj nazwe pliku tekstowego z rozszerzeniem:")

with open(f"lab_1\{file_name}", "r") as file:
    lines = file.read().splitlines()

    numb = []
    for line in lines:
        numb.extend([int(num) for num in line.split()])  
    
    new_lines = [re.sub(" ", "-", line) for line in lines]


first_line = lines[0]
first_value = int(first_line.split()[0])
second_value = int(first_line.split()[1])

dist_numb = sorted(list(dict.fromkeys(numb[2:])))

# ZADANIE 1

print(f"Rząd grafu G wynosi {first_value}")
print(f"Zbior wierzcholkow V = {set(dist_numb)}\n")

print(f"Rozmiar grafu G wynosi {second_value}")
print(f"Zbior krawedzi E = {set(new_lines[1:])}\n")

zero_matrix = np.zeros((first_value,first_value))
relation_list = []
point_list = []
for line in lines[1:]:
    a = line.split(" ")
    x = int(a[0]) 
    y = int(a[1])
    zero_matrix[(x-1),(y-1)] = 1
    zero_matrix[(y-1),(x-1)] = 1

print("Macierz sąsiedztwa A = ")
print(f"{zero_matrix}\n")

zero_matrix_2 = np.zeros((first_value,second_value))

for x in range(1,first_value+1):
    column = 0
    for char in lines[1:]:
        column +=1
        y = int(char.split(" ")[0])
        z = int(char.split(" ")[1])
        if x == y or x == z:
            zero_matrix_2[(x-1,column-1)] = 1        

print("Macierz incydencji M = ")
print(zero_matrix_2)

# # ZADANIE 2

print(f"Rząd grafu G wynosi {first_value}\n")
print(f"Rozmiar grafu G wynosi {second_value}\n")

print(f"Stopnie wierzchołków:")
w = 0
sequence = []
for x in range(1,first_value+1):
    w += 1
    numb = 0
    for char in lines[1:]: 
        v1 = int(char.split(" ")[0])
        v2 = int(char.split(" ")[1])
        if x == v1 or x == v2:
            numb += 1
    sequence.append(numb)
    print(f"deg({w})={numb}")
print(f"Ciag stopni grafu G: {sorted(sequence)}")

#ZADANIE 3

graf_ogolny = False

#sprawdza pętle własne
for char in lines[1:]: 
    v1 = char.split(" ")[0]
    v2 = char.split(" ")[1]
    if v1 == v2:
        graf_ogolny = True

#sprawdza krawędzie równoległe
lines_sorted = [tuple(sorted(char.split())) for char in lines[1:]]

if len(lines_sorted) != len(set(lines_sorted)):
    graf_ogolny = True

if graf_ogolny == True:
    print("Graf G jest grafem ogólnym.")
else:
    print("Graf G jest grafem prostym.")


# #ZADANIE 4

graf_pelny = []

for i in range(1,(first_value+1)):
        for j in range(i+1,(first_value+1)):
            graf_pelny.append(f"{i} {j}")

if sorted(lines[1:]) == graf_pelny:
     print("Graf G jest grafem pełnym")
else:
     print("Graf G nie jest grafem pełnym\n")
     brakujace = list(set(graf_pelny) - set(sorted(lines[1:])))
     print(f"Krawędzie dopełnienia grafu G:{brakujace}")

#ZADANIE 5

lista_sasiedztwa = []
for i in range(first_value + 1):
    lista_sasiedztwa.append([])

for line in lines[1:]:
    parts = line.split()
    v1 = int(parts[0])
    v2 = int(parts[1])

    lista_sasiedztwa[v1].append(v2)
    lista_sasiedztwa[v2].append(v1)

print("Lista sasiedztwa:")
for i in range(1, first_value + 1):
    print(f"{i}-> {sorted(lista_sasiedztwa[i])}")
