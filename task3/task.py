import math

def parse_opinion_csv(opinion_str):
    edges = []
    for line in opinion_str.strip().splitlines():
        opinions = list(map(int, line.split(',')))
        edges.append(opinions)
    return edges

def entropy(edges):
    n = len(edges)
    k = len(edges[0])
    result = 0
    for i in range(n):
        for j in range(k):
            p = edges[j][i] / (n - 1)
            if p > 0:
                result -= p * math.log2(p)
    return result

def main(opinion_str):
    edges = parse_opinion_csv(opinion_str)
    return entropy(edges)

if __name__ == "__main__":
    opinion_str = """
    2,0,2,0,0
    0,1,0,0,1
    2,1,0,0,1
    0,1,0,1,1
    0,1,0,1,1
    """
    print(main(opinion_str))