"""
Problem Chińskiego Listonosza
- każda krawędź musi być odwiedzona co najmniej raz
- trasa musi być zamknięta (wraca do startu)
- szukamy trasy o minimalnej sumie wag
"""


# ── Wczytaj graf z pliku ──────────────────────────────────────────────────────

def wczytaj_graf(plik):
    with open(plik) as f:
        linie = f.read().splitlines()

    v, e = map(int, linie[0].split())
    krawedzie = []
    for linia in linie[1:e+1]:
        u, w, waga = map(int, linia.split())
        krawedzie.append((u, w, waga))
    return v, krawedzie


# ── Dijkstra: najkrótsza ścieżka od źródła do wszystkich wierzchołków ─────────

def dijkstra(adj, zrodlo, n):
    dist = [float('inf')] * (n + 1)
    prev = [None] * (n + 1)
    dist[zrodlo] = 0
    odwiedzone = [False] * (n + 1)

    for _ in range(n):
        # Znajdź nieodwiedzony wierzchołek z najmniejszym dystansem (przegląd całej listy)
        u = None
        for i in range(1, n + 1):
            if not odwiedzone[i] and (u is None or dist[i] < dist[u]):
                u = i

        if dist[u] == float('inf'):
            break  # pozostałe wierzchołki są nieosiągalne

        odwiedzone[u] = True
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    return dist, prev


def odtworz_sciezke(prev, cel):
    sciezka = []
    while cel is not None:
        sciezka.append(cel)
        cel = prev[cel]
    return list(reversed(sciezka))


# ── Minimalne parowanie wierzchołków o nieparzystym stopniu (brute-force) ─────
# Liczba takich wierzchołków jest zawsze parzysta i zwykle mała

def min_parowanie(nieparzyste, dist):
    if not nieparzyste:
        return [], 0

    best_koszt = [float('inf')]
    best_pary  = [[]]

    def szukaj(pozostale, pary, koszt):
        if not pozostale:
            if koszt < best_koszt[0]:
                best_koszt[0] = koszt
                best_pary[0]  = pary[:]
            return
        u = pozostale[0]
        for i in range(1, len(pozostale)):
            v = pozostale[i]
            nowe = [x for j, x in enumerate(pozostale) if j != 0 and j != i]
            szukaj(nowe, pary + [(u, v)], koszt + dist[u][v])

    szukaj(nieparzyste, [], 0)
    return best_pary[0], best_koszt[0]


# ── Algorytm Hierholzera: obwód Eulera w multigrafie ─────────────────────────

def euler(adj, start):
    # Kopiujemy listy sąsiedztwa żeby je modyfikować
    adj = {u: list(s) for u, s in adj.items()}
    stos, obwod = [start], []

    while stos:
        u = stos[-1]
        if adj.get(u):
            v, w = adj[u].pop()
            # Usuń krawędź w drugą stronę
            for i, (x, wx) in enumerate(adj.get(v, [])):
                if x == u and wx == w:
                    adj[v].pop(i)
                    break
            stos.append(v)
        else:
            obwod.append(stos.pop())

    return list(reversed(obwod))


# ── Zapis do pliku Graphviz ───────────────────────────────────────────────────

def zapisz_gv(krawedzie, plik):
    with open(plik, 'w') as f:
        f.write("graph G {\n")
        for u, v, w in krawedzie:
            f.write(f'    {u} -- {v} [label="{w}"];\n')
        f.write("}\n")


# ── MAIN ─────────────────────────────────────────────────────────────────────

n, krawedzie = wczytaj_graf("lab_4/graf.txt")

# Buduj listę sąsiedztwa – dla każdego wierzchołka inicjalizujemy pustą listę
adj = {i: [] for i in range(1, n+1)}
for u, v, w in krawedzie:
    adj[u].append((v, w))
    adj[v].append((u, w))

# Znajdź wierzchołki o nieparzystym stopniu
stopien = {i: 0 for i in range(1, n+1)}
for u, v, _ in krawedzie:
    stopien[u] += 1
    stopien[v] += 1
nieparzyste = [u for u in range(1, n+1) if stopien[u] % 2 == 1]

# Oblicz najkrótsze ścieżki między każdą parą wierzchołków nieparzystych
dist  = {}
prevs = {}
for u in nieparzyste:
    dist[u], prevs[u] = dijkstra(adj, u, n)

# Znajdź minimalne parowanie
pary, koszt_extra = min_parowanie(nieparzyste, dist)

# Dodaj duplikaty krawędzi dla wyrównania stopni (multigraf)
multi_adj = {i: [] for i in range(1, n+1)}
for u, v, w in krawedzie:
    multi_adj[u].append((v, w))
    multi_adj[v].append((u, w))

for u, v in pary:
    sciezka = odtworz_sciezke(prevs[u], v)
    for i in range(len(sciezka) - 1):
        a, b = sciezka[i], sciezka[i+1]
        # Znajdź wagę krawędzi a-b
        w = next(ww for (x, ww) in adj[a] if x == b)
        multi_adj[a].append((b, w))
        multi_adj[b].append((a, w))

# Znajdź obwód Eulera
obwod = euler(multi_adj, krawedzie[0][0])

# Wyniki
suma = sum(w for _, _, w in krawedzie)
print("Trasa:", " -- ".join(map(str, obwod)))
print(f"Suma krawędzi: {suma}, koszt dodatkowy: {koszt_extra}, łącznie: {suma + koszt_extra}")

zapisz_gv(krawedzie, "gv.txt")
print("Graf zapisany do gv.txt")