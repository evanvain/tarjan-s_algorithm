def tarjan_scc(graph):
    index = {}
    lowlink = {}
    stack = []
    on_stack = set()
    time = [0]
    components = []

    def strong_connect(v):
        index[v] = time[0]
        lowlink[v] = time[0]
        time[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, []):
            if w not in index:
                strong_connect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            components.append(component)

    for v in graph:
        if v not in index:
            strong_connect(v)
    return components

graph = {
    'A': ['B'],
    'B': ['C'],
    'C': ['A'],
    'D': []
}
print(tarjan_scc(graph))