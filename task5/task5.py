import json

def main(json_str_a, json_str_b):
    def parse_ranking(json_str):
        ranking_list = json.loads(json_str)
        element_to_rank = {}
        rank = 1
        for item in ranking_list:
            if isinstance(item, list):
                for elem in item:
                    element_to_rank[elem] = rank
            else:
                element_to_rank[item] = rank
            rank += 1
        return element_to_rank

    element_to_rank_A = parse_ranking(json_str_a)
    element_to_rank_B = parse_ranking(json_str_b)
    elements = set(element_to_rank_A.keys()).union(set(element_to_rank_B.keys()))

    inversions = set()
    element_list = sorted(elements)
    for i in range(len(element_list)):
        for j in range(i+1, len(element_list)):
            elem_i = element_list[i]
            elem_j = element_list[j]
            
            rankA_i = element_to_rank_A.get(elem_i)
            rankA_j = element_to_rank_A.get(elem_j)
    
            rankB_i = element_to_rank_B.get(elem_i)
            rankB_j = element_to_rank_B.get(elem_j)
           
            if rankA_i is None or rankA_j is None or rankB_i is None or rankB_j is None:
                continue
            diffA = rankA_i - rankA_j
            diffB = rankB_i - rankB_j
            if diffA * diffB < 0:
                inversions.add(elem_i)
                inversions.add(elem_j)
    return sorted(inversions)


if __name__ == "__main__":
    json_str_a = '[1,[2,3],4,[5,6,7],8,9,10]'
    # Потребовалось сделать json строку валидной
    json_str_b = '[[1,2],[3,4,5],6,7,9,[8,10]]'

    print(main(json_str_a, json_str_b))  # Output: [8, 9]
