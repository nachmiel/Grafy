import os

os.system('cls' if os.name == 'nt' else 'clear')

file = open("lab_4/graf.txt", "r")
lines = file.read().splitlines()
file.close()

n = int(lines[0].split()[0])

adj = []
for i in range(n):
    adj.append([])

edges = []

for i in range(1, len(lines)):
    u, v, w = map(int, lines[i].split())
    u -= 1
    v -= 1

    adj[u].append(v)
    adj[v].append(u)

    edges.append((u, v))

deg = [0] * n

for u, v in edges:
    deg[u] += 1
    deg[v] += 1

odd = []
for i in range(n):
    if deg[i] % 2 == 1:
        odd.append(i)

# kopia grafu
g = {}
for i in range(n):
    g[i] = []

for u, v in edges:
    g[u].append(v)
    g[v].append(u)

# dodajemy krawędź między nieparzystymi
u = odd[0]
v = odd[1]
g[u].append(v)
g[v].append(u)

# sortujemy żeby wynik był stały
for i in g:
    g[i].sort()

def euler(start):
    stack = [start]
    path = []

    local = {}
    for i in g:
        local[i] = g[i][:]

    while stack:
        v = stack[-1]

        if local[v]:
            u = local[v].pop(0)
            local[u].remove(v)
            stack.append(u)
        else:
            path.append(stack.pop())

    return path[::-1]

cycle = euler(0)

print([x + 1 for x in cycle])