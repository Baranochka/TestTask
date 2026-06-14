import csv
import ast
import matplotlib.pyplot as plt
class Player():
    def __init__(self):
        self.count_records = 0
        self.total_time_stalls_duration = 0
        self.total_time_playback = 0
        self.total_time_hight_quality = 0 
        self.total_time_low_quality = 0
        self.list_stalls_duration = []
        self.total_switch_quality = 0
         
    def AverageDelayTime(self):
        return self.total_time_stalls_duration // self.count_records
    
    def AveragePlaybackTime(self):
        return self.total_time_playback // self.count_records

    def AverageCountSwitchQuality(self):
        return self.total_switch_quality // self.count_records
    
    def PercentageDelay(self):
        return round((self.total_time_stalls_duration / (self.total_time_stalls_duration + self.total_time_playback)) * 100)
    
    def PercentagePlaybackHightQuality(self):
        return round((self.total_time_hight_quality / self.total_time_playback) * 100)
    
    def PercentagePlaybackLowQuality(self):
        return round((self.total_time_low_quality / self.total_time_playback) * 100)

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
    pl1 = Player()
    pl2 = Player()
    quality={'144p':1,
             '240p':2,
             '360p':3,
             '480p':4,
             '720p':5,
             '1080p':6,
             }
    
    for row in data:
        if row[0] == 'player_1':
            if row[2] != []:
                for i, a in enumerate(row[2]):
                    if a not in ['UNKNOWN','LOW_VERTICAL']:
                        if quality[a]>3:
                            pl1.total_time_hight_quality+=(row[3][i]*1000)
                        else:
                            pl1.total_time_low_quality+=(row[3][i]*1000)
                pl1.total_switch_quality+=(len(row[2])-1)
            if row[3] != []:
                for a in row[3]:
                    pl1.total_time_playback+=(a*1000)
            pl1.total_time_stalls_duration += row[1]
            pl1.list_stalls_duration.append(row[1])
            pl1.count_records +=1
        elif row[0] == 'player_2':
            if row[2] != []:
                for i, a in enumerate(row[2]):
                    if a not in ['UNKNOWN','LOW_VERTICAL']:
                        if quality[a]>3:
                            pl2.total_time_hight_quality+=(row[3][i]*1000)
                        else:
                            pl2.total_time_low_quality+=(row[3][i]*1000)
                pl2.total_switch_quality+=(len(row[2])-1)
            if row[3] != []:
                for a in row[3]:
                    pl2.total_time_playback+=(a*1000)
            pl2.total_time_stalls_duration += row[1]
            pl2.list_stalls_duration.append(row[1])
            pl2.count_records +=1
    print(f'Cреднее время задержки плеера 1: {pl1.AverageDelayTime()} мс = {pl1.AverageDelayTime()//1000} с')
    print(f'Cреднее время задержки плеера 2: {pl2.AverageDelayTime()} мс = {pl2.AverageDelayTime()//1000} с')
    print(f'Cреднее время воспроизведения плеера 1: {pl1.AveragePlaybackTime()} мс = {pl1.AveragePlaybackTime()//1000} с')
    print(f'Cреднее время воспроизведения плеера 2: {pl2.AveragePlaybackTime()} мс = {pl2.AveragePlaybackTime()//1000} с')
    print(f'Процент задержки плеера 1: {pl1.PercentageDelay()}%')
    print(f'Процент задержки плеера 2: {pl2.PercentageDelay()}%')
    print(f'Процент просмотра видео в высоком качестве плеера 1: {pl1.PercentagePlaybackHightQuality()}%')
    print(f'Процент просмотра видео в высоком качестве плеера 2: {pl2.PercentagePlaybackHightQuality()}%')
    print(f'Среднее количество переключений качества плеера 1: {pl1.AverageCountSwitchQuality()}')
    print(f'Среднее количество переключений качества плеера 2: {pl2.AverageCountSwitchQuality()}')

    sorted_data = sorted(pl1.list_stalls_duration)  
    ecdf = [i/pl1.count_records for i in range(pl1.count_records)]  
    plt.step(sorted_data, ecdf, color='red', label='Player 1')
    sorted_data = sorted(pl2.list_stalls_duration) 
    ecdf = [i/pl2.count_records for i in range(pl2.count_records)]  
    plt.step(sorted_data, ecdf, color='green', label='Player 2')
    plt.ylim(0, 1)  
    plt.xlim(0, 60000)  
    plt.xlabel('t, мс')
    plt.ylabel('F(t)')
    plt.title('Функция распределения')
    plt.legend(loc='lower right', fontsize='small', fancybox=True)
    plt.show()
    
if __name__ == "__main__":
    main()
