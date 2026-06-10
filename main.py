import csv
import ast

def read_csv_file() -> list:
    data = []
    with open("player_stalls.csv") as csvfile:
        csvdata = csv.reader(csvfile, delimiter=';')
        for rows in csvdata:
            row = []
            if rows[0] in ['player_1','player_2']:
                row.append(rows[0])
                row.append(int(rows[1]))
                row.append(ast.literal_eval(rows[2]))
                temp = rows[3][:rows[3].index(']') + 1]
                row.append(ast.literal_eval(temp))
                data.append(row)
    return data

def main():
    data = read_csv_file()


if __name__ == "__main__":
    main()
