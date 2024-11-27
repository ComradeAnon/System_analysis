import csv

def main(file_path, row_number, column_number):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)
        print(rows[row_number][column_number])
    
if __name__ == "__main__":
    main("C:\\Users\\Comra\\Python\\sys_analize\\System_analysis\\task1\\example.csv", 1, 1)