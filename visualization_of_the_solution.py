import networkx as nx
import matplotlib.pyplot as plt

class TarjanVisualizer:
    def __init__(self, G):
        self.G = G
        self.index = 0
        self.stack = []
        self.on_stack = set()
        self.indices = {}
        self.lowlink = {}
        self.steps = []

    def run(self):
        for v in self.G.nodes():
            if v not in self.indices:
                yield from self._strongconnect(v)
        snapshot = self._snapshot(None, 'Finished')
        self.steps.append(snapshot)
        yield snapshot

    def _strongconnect(self, v):
        self.indices[v] = self.index
        self.lowlink[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.on_stack.add(v)

        snapshot = self._snapshot(v, 'init')
        self.steps.append(snapshot)
        yield snapshot

        for w in self.G[v]:
            if w not in self.indices:
                yield from self._strongconnect(w)
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w])
                snapshot = self._snapshot(v, f'post-recursion to {w}')
                self.steps.append(snapshot)
                yield snapshot
            elif w in self.on_stack:
                self.lowlink[v] = min(self.lowlink[v], self.indices[w])
                snapshot = self._snapshot(v, f'back-edge to {w}')
                self.steps.append(snapshot)
                yield snapshot

        if self.lowlink[v] == self.indices[v]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            snapshot = self._snapshot(v, f'found SCC {scc}')
            self.steps.append(snapshot)
            yield snapshot

    def _snapshot(self, current, action):
        color_map = []
        labels = {}
        for node in self.G.nodes():
            if node == current:
                color_map.append('red')
            elif node in self.on_stack:
                color_map.append('orange')
            elif node in self.indices:
                color_map.append('lightblue')
            else:
                color_map.append('white')
            labels[node] = f"idx:{self.indices.get(node, '-')}, low:{self.lowlink.get(node, '-')}"
        return {
            'color_map': color_map,
            'labels': labels,
            'stack': list(self.stack),
            'action': action
        }

def draw_step(G, pos, state, step_num):
    plt.figure(figsize=(6, 4))
    plt.axis('off')
    plt.title(f"Step {step_num}: {state['action']}")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos, node_color=state['color_map'], edgecolors='black')
    nx.draw_networkx_labels(G, pos, labels=state['labels'])
    stack_str = ', '.join(map(str, state['stack'])) or '—'
    plt.text(0.95, 0.5, f"Stack:\n{stack_str}",
             transform=plt.gca().transAxes,
             verticalalignment='center',
             horizontalalignment='right')
    plt.show()

def main():
    G = nx.DiGraph()
    G.add_edges_from([
        (1, 2), (2, 3), (3, 1),
        (2, 4), (4, 5), (5, 4)
    ])

    pos = nx.spring_layout(G, seed=42)

    viz = TarjanVisualizer(G)

    for step_num, state in enumerate(viz.run()):
        draw_step(G, pos, state, step_num)

if __name__ == '__main__':
    main()