from collections import defaultdict

# Парсим строку. Считаем что вершины обладают уникальными целыми номерами
def parse_graph(graph_str):
    edges = []
    for line in graph_str.strip().splitlines():
        parent, child = map(int, line.split(','))
        edges.append((parent, child))
    return edges

# Построим дерево, и найдем корень
def build_tree(edges):
    tree = defaultdict(list)
    parents = {}
    all_nodes = set()
    
    for parent, child in edges:
        tree[parent].append(child)
        parents[child] = parent
        all_nodes.add(parent)
        all_nodes.add(child)
    
    # Найдем корень - вершину, которая не является ребенком
    root = next(node for node in all_nodes if node not in parents)
    return tree, root

# Обход в глубину
def dfs(tree, node, parent, level, result, levels_count):
    children = tree[node]
    # r1 - количество детей
    r1 = len(children)
    
    # r2 - количество родителей (всегда 1, если не корень)
    r2 = 0 if parent is None else 1
    
    # r4 - количество предков (равно глубине от корня)
    r4 = level
    
    # r5 - количество вершин на том же уровне
    if level not in levels_count:
        levels_count[level] = 0
    levels_count[level] += 1
    
    # r3 - количество потомков (считаем их в процессе обхода)
    descendants_count = 0
    for child in children:
        descendants_count += dfs(tree, child, node, level + 1, result, levels_count) + 1
    
    result[node] = (r1, r2, descendants_count - r1, r4, 0)  # r5 пока 0, обновим потом
    
    return descendants_count

# r5. Также именно здесь корректируется значение r4
def assign_level_counts(result, levels_count):
    for node, (r1, r2, r3, r4, _) in result.items():
        result[node] = (r1, r2, r3, r4 - r2, levels_count[r4] - 1)

def main(graph_str: str) -> str:
    edges = parse_graph(graph_str)
    tree, root = build_tree(edges)
    
    result = {}
    levels_count = {}
    
    # Запуск DFS от корня
    dfs(tree, root, None, 0, result, levels_count)
    
    # Присвоение количества вершин на каждом уровне
    assign_level_counts(result, levels_count)
    
    sorted_result = dict(sorted(result.items()))
    csv_lines = []
    for _, (r1, r2, r3, r4, r5) in sorted_result.items():
        csv_lines.append(f"{r1},{r2},{r3},{r4},{r5}")
    return "\n".join(csv_lines)


# Пример использования:
if __name__ == "__main__":
    graph_str = """
    1,2
    1,3
    3,4
    3,5
    """

    result = main(graph_str)
    print(result)