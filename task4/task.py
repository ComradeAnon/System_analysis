import csv
import math

def main():
    filename = 'data.csv'
    counts = {}
    age_groups = []
    categories = []
    total_count = 0

    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        categories = header[1:]

        for row in reader:
            if not row or not row[0].strip():
                continue
            age_group = row[0]
            if age_group not in age_groups:
                age_groups.append(age_group)
            for i, count_str in enumerate(row[1:]):
                category = categories[i]
                count = int(count_str)
                counts[(age_group, category)] = count
                total_count += count

    joint_probs = {}
    for (age_group, category), count in counts.items():
        joint_probs[(age_group, category)] = count / total_count

    P_A = {}
    for age_group in age_groups:
        P_A[age_group] = 0.0
    for (age_group, category), p in joint_probs.items():
        P_A[age_group] += p

    P_B = {}
    for category in categories:
        P_B[category] = 0.0
    for (age_group, category), p in joint_probs.items():
        P_B[category] += p
    H_AB = 0.0
    for p in joint_probs.values():
        if p > 0:
            H_AB -= p * math.log2(p)
    H_A = 0.0
    for p in P_A.values():
        if p > 0:
            H_A -= p * math.log2(p)
    H_B = 0.0
    for p in P_B.values():
        if p > 0:
            H_B -= p * math.log2(p)
    Ha_B = H_AB - H_A
    I_AB = H_B - Ha_B
    
    result = [H_AB, H_A, H_B, Ha_B, I_AB]

    return result

if __name__ == "__main__":
    result = main()
    print(result)