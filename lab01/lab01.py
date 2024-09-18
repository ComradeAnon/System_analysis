import json
import pandas as pd

# Чтение JSON файла
def read_json_graph(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
    
def main():
    # Получение данных в формате JSON
    graph_data = read_json_graph('nodes.json')
    # Преобразование данных от туда в словарь
    nodes = graph_data["nodes"]
    # Получение списка вершин, все вершины имеют строковое название
    node_names = sorted(nodes.keys())
    # Матрицу смежности будем хранить как пандас датафрейм, столбцы и индексы которого - вершины графа
    adjacency_df = pd.DataFrame(0, index=node_names, columns=node_names)
    # Заполнение матрицы
    for node, neighbors in nodes.items():
        for neighbor in neighbors:
            adjacency_df.loc[node, neighbor] = 1
    # Вывод матрицы
    print(adjacency_df)

if __name__ == "__main__":
    main()