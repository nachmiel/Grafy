plik = "lab_4/graf.txt"

def wczytaj_graf(plik):
    with open(plik) as f:
        linie = f.read().splitlines()

    v, e = map(int, linie[0].split())

    krawedzie = []
    for i in range(1, e + 1):
        u, w, waga = map(int, linie[i].split())
        krawedzie.append((u, w, waga))

    return v, krawedzie


#  Dijkstra – najkrótsza ścieżka od źródła do pozostałych

def dijkstra(lista_sasiedztwa, start, n):
    odleglosc = [float('inf')] * (n + 1)
    poprzedni = [None] * (n + 1)
    odwiedzone = [False] * (n + 1)
    odleglosc[start] = 0

    for _ in range(n):
        # Znajdź nieodwiedzony wierzchołek z najmniejszą odległością
        u = None
        for i in range(1, n + 1):
            if not odwiedzone[i]:
                if u is None or odleglosc[i] < odleglosc[u]:
                    u = i

        # Jeśli najlepsza odległość to nieskończoność – reszta nieosiągalna
        if odleglosc[u] == float('inf'):
            break

        odwiedzone[u] = True

        # Zaktualizuj odległości sąsiadów
        for sasiad, waga in lista_sasiedztwa[u]:
            nowa_odleglosc = odleglosc[u] + waga
            if nowa_odleglosc < odleglosc[sasiad]:
                odleglosc[sasiad] = nowa_odleglosc
                poprzedni[sasiad] = u

    return odleglosc, poprzedni


# Odtwarza listę wierzchołków tworzących ścieżkę do celu
def odtworz_sciezke(poprzedni, cel):
    sciezka = []
    aktualny = cel
    while aktualny is not None:
        sciezka.append(aktualny)
        aktualny = poprzedni[aktualny]
    sciezka.reverse()
    return sciezka


#  Minimalne parowanie wierzchołków o nieparzystym stopniu
#  (brute-force – działa dobrze gdy takich wierzchołków jest mało)

def min_parowanie(nieparzyste, odleglosci):
    if not nieparzyste:
        return [], 0

    najlepszy_koszt = float('inf')
    najlepsze_pary = []

    def szukaj(pozostale, aktualne_pary, aktualny_koszt):
        nonlocal najlepszy_koszt, najlepsze_pary

        # Wszystkie wierzchołki sparowane – sprawdź czy to najlepszy wynik
        if not pozostale:
            if aktualny_koszt < najlepszy_koszt:
                najlepszy_koszt = aktualny_koszt
                najlepsze_pary = aktualne_pary[:]
            return

        # Sparuj pierwszy wierzchołek z każdym pozostałym
        pierwszy = pozostale[0]
        for i in range(1, len(pozostale)):
            drugi = pozostale[i]
            # Pozostałe wierzchołki po usunięciu tej pary
            reszta = [x for j, x in enumerate(pozostale) if j != 0 and j != i]
            dodatkowy_koszt = odleglosci[pierwszy][drugi]
            szukaj(reszta, aktualne_pary + [(pierwszy, drugi)], aktualny_koszt + dodatkowy_koszt)

    szukaj(nieparzyste, [], 0)
    return najlepsze_pary, najlepszy_koszt

#  Algorytm Hierholzera – szukanie obwodu Eulera w multigrafie

def znajdz_obwod_eulera(lista_sasiedztwa, start):
    # Kopia listy sąsiedztwa – będziemy usuwać krawędzie
    kopia = {}
    for u in lista_sasiedztwa:
        kopia[u] = list(lista_sasiedztwa[u])

    stos = [start]
    obwod = []

    while stos:
        u = stos[-1]
        if kopia.get(u):
            # Idź po następnej dostępnej krawędzi
            v, w = kopia[u].pop()
            # Usuń krawędź w przeciwnym kierunku
            for i, (x, wx) in enumerate(kopia.get(v, [])):
                if x == u and wx == w:
                    kopia[v].pop(i)
                    break
            stos.append(v)
        else:
            # Brak krawędzi – dodaj do obwodu
            obwod.append(stos.pop())

    obwod.reverse()
    return obwod


#  Zapis grafu do pliku Graphviz (.gv)


def zapisz_graphviz(krawedzie, plik_wyjsciowy):
    with open(plik_wyjsciowy, 'w') as f:
        f.write("graph G {\n")
        for u, v, w in krawedzie:
            f.write(f'    {u} -- {v} [label="{w}"];\n')
        f.write("}\n")


#MAIN

# 1. Wczytaj graf
n, krawedzie = wczytaj_graf(plik)

# 2. Zbuduj listę sąsiedztwa
lista_sasiedztwa = {i: [] for i in range(1, n + 1)}
for u, v, w in krawedzie:
    lista_sasiedztwa[u].append((v, w))
    lista_sasiedztwa[v].append((u, w))

# 3. Znajdź wierzchołki o nieparzystym stopniu
stopien = {i: 0 for i in range(1, n + 1)}
for u, v, _ in krawedzie:
    stopien[u] += 1
    stopien[v] += 1

nieparzyste = [u for u in range(1, n + 1) if stopien[u] % 2 == 1]
print(f"Wierzchołki o nieparzystym stopniu: {nieparzyste}")

# 4. Oblicz najkrótsze ścieżki między każdą parą wierzchołków nieparzystych
odleglosci = {}
poprzednie = {}
for u in nieparzyste:
    odleglosci[u], poprzednie[u] = dijkstra(lista_sasiedztwa, u, n)

# 5. Znajdź minimalne parowanie (najmniejszy koszt dodatkowych krawędzi)
pary, koszt_dodatkowy = min_parowanie(nieparzyste, odleglosci)
print(f"Dobrane pary: {pary}, koszt dodatkowy: {koszt_dodatkowy}")

# 6. Zbuduj multigraf – dodaj duplikaty krawędzi dla par
multigraf = {i: [] for i in range(1, n + 1)}
for u, v, w in krawedzie:
    multigraf[u].append((v, w))
    multigraf[v].append((u, w))

for u, v in pary:
    sciezka = odtworz_sciezke(poprzednie[u], v)
    for i in range(len(sciezka) - 1):
        a = sciezka[i]
        b = sciezka[i + 1]
        # Znajdź wagę krawędzi a-b w oryginalnym grafie
        waga = None
        for (sasiad, w) in lista_sasiedztwa[a]:
            if sasiad == b:
                waga = w
                break
        multigraf[a].append((b, waga))
        multigraf[b].append((a, waga))

# 7. Znajdź obwód Eulera (trasę listonosza)
start = krawedzie[0][0]
trasa = znajdz_obwod_eulera(multigraf, start)

# 8. Wyświetl wyniki
suma_krawedzi = sum(w for _, _, w in krawedzie)
print("Trasa:", " -> ".join(map(str, trasa)))
print(f"Suma wag wszystkich krawędzi: {suma_krawedzi}")
print(f"Koszt dodatkowych przejść:    {koszt_dodatkowy}")
print(f"Łączny koszt trasy:           {suma_krawedzi + koszt_dodatkowy}")

# 9. Zapisz graf do pliku Graphviz
zapisz_graphviz(krawedzie, "gv.txt")