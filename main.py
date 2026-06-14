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
    
    quality={'144p':1,
             '240p':2,
             '360p':3,
             '480p':4,
             '720p':5,
             '1080p':6,
             }
    
    time_stalls_duration_1 = 0
    time_stalls_duration_2 = 0
    count_1 = 0
    count_2 = 0
    total_playback_time_1 = 0
    total_playback_time_2 = 0
    for row in data:
        if row[0] == 'player_1':
            time_quality_hight=0
            time_quality_low=0
            if row[2] != []:
                for i, a in enumerate(row[2]):
                    if a not in ['UNKNOWN','LOW_VERTICAL']:
                        if quality[a]>3:
                            time_quality_hight+=row[3][i]
                        else:
                            time_quality_low+=row[3][i]
            playback_time=0
            if row[3] != []:
                for a in row[3]:
                    playback_time+=a
            total_playback_time_1+=playback_time
            time_stalls_duration_1 += row[1]
            count_1+=1
        elif row[0] == 'player_2':
            playback_time=0
            for a in row[3]:
                playback_time+=a
            total_playback_time_2+=playback_time
            count_2+=1
            time_stalls_duration_2 += row[1]
    print('Общее и среднее время задержки плеера 1: ', time_stalls_duration_1, int(time_stalls_duration_1/count_1))
    print('Общее и среднее время задержки плеера 1: ', time_stalls_duration_2, int(time_stalls_duration_2/count_2))
    print('Общее и среднее время воспроизведение плеера 1: ',total_playback_time_1, int(total_playback_time_1/count_1))
    print('Общее и среднее время воспроизведение плеера 2: ',total_playback_time_2, int(total_playback_time_2/count_2))
    print('Процент задержки плеера 1: ', time_stalls_duration_1/(time_stalls_duration_1+total_playback_time_1))
    print('Процент задержки плеера 2: ', time_stalls_duration_2/(time_stalls_duration_2+total_playback_time_2))
if __name__ == "__main__":
    main()
