import json
import numpy as np

def membership_degree(x, points):
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        if x0 <= x <= x1:
            if x1 == x0:
                return y0  # Избежание деления на 0
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 0.0

def fuzzify(value, fuzzy_sets):
    memberships = {}
    for fuzzy_set in fuzzy_sets:
        memberships[fuzzy_set['id']] = membership_degree(value, fuzzy_set['points'])
    return memberships

def apply_rules(temp_membership, rules, heating_fuzzy_sets):
    output_membership = {fs['id']: 0.0 for fs in heating_fuzzy_sets}
    for temp_term, heating_term in rules:
        if temp_term in temp_membership:
            degree = temp_membership[temp_term]
            output_membership[heating_term] = max(output_membership[heating_term], degree)
    return output_membership

def defuzzify(fuzzy_output, heating_fuzzy_sets):
    numerator = 0.0
    denominator = 0.0
    for heating_set in heating_fuzzy_sets:
        set_id = heating_set['id']
        max_degree = fuzzy_output[set_id]
        for i in range(len(heating_set['points']) - 1):
            x0, y0 = heating_set['points'][i]
            x1, y1 = heating_set['points'][i + 1]
            if max_degree > 0:
                # Вычисление центра тяжести для текущего сегмента
                x_segment = np.linspace(x0, x1, 100)
                y_segment = np.minimum(np.interp(x_segment, [x0, x1], [y0, y1]), max_degree)
                numerator += np.sum(x_segment * y_segment)
                denominator += np.sum(y_segment)
    return numerator / denominator if denominator != 0 else 0.0

def main(temp_json, heating_json, rules_json, current_temp):
    temperature_sets = json.loads(temp_json)['температура']
    heating_sets = json.loads(heating_json)['уровень нагрева']
    rules = json.loads(rules_json)

    # Фаззификация текущей температуры
    temp_membership = fuzzify(current_temp, temperature_sets)

    # Применение правил управления
    fuzzy_output = apply_rules(temp_membership, rules, heating_sets)

    # Дефаззификация для получения чёткой величины
    optimal_heating = defuzzify(fuzzy_output, heating_sets)

    return optimal_heating

if __name__== "__main__":
    temp_json = """
    {
    "температура": [
        {
        "id": "холодно",
        "points": [
            [0,1],
            [18,1],
            [22,0],
            [50,0]
        ]
        },
        {
        "id": "комфортно",
        "points": [
            [18,0],
            [22,1],
            [24,1],
            [26,0]
        ]
        },
        {
        "id": "жарко",
        "points": [
            [0,0],
            [24,0],
            [26,1],
            [50,1]
        ]
        }
    ]
    }
    """

    heating_json = """
    {
    "уровень нагрева": [ 
        {
            "id": "слабый",
            "points": [
                [0,0],
                [0,1],
                [5,1],
                [8,0]
            ]
        },
        {
            "id": "умеренный",
            "points": [
                [5,0],
                [8,1],
                [13,1],
                [16,0]
            ]
        },
        {
            "id": "интенсивный",
            "points": [
                [13,0],
                [18,1],
                [23,1],
                [26,0]
            ]
        }
    ]
    }
    """

    rules_json = """
    [
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ]
    """
    current_temp = 20
    result = main(temp_json, heating_json, rules_json, current_temp)
    print(f"Оптимальный уровень нагрева: {result}")