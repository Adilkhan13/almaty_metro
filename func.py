import pandas as pd
import datetime

# TODO 
#   Нет времени остановки на станции
#   Нет времени пути между станциями (взяли дефолт в 5 минут)
#   Нет рассписания для выходных и часов пик (*возможно оно отличется от предоставленного)

# Отсортированный массив веток Алматинского метрополитена
STATIONS_LIST = (
    'BM',
    'SA',
    'MSK',
    'SRN',
    'ALA',
    'TEATR',
    'BKNR',
    'ABA',
    'ALM',
    'ZZ',
    'RMBK'
)

# Входные данные
# TODO Насколько я знаю в выходные другое расписание, но данные так же не были предоставленны
def get_schedule_df()->pd.DataFrame:
    "Выгружем данные"
    df = pd.read_csv("./data/metro_schedule.csv",sep = ';', header=None).iloc[:,1:-1]
    df.columns = ['from','arrival_time','to']
    df = df[df['arrival_time'].str[:2] !='24']
    df['arrival_time'] = pd.to_datetime(df['arrival_time'], format="%H:%M:%S").dt.time
    return df

df = get_schedule_df()
curr_time = datetime.datetime.today().time()
start_position = 'MSK'
end_position = 'RMBK'
################################################


def trip_duration(
        df:pd.DataFrame,
        curr_time:datetime.time,
        start_position:str,
        end_position:str,
        stations_list = STATIONS_LIST
        )->datetime.time:
    """
    attr:
        df: Расписание
        curr_time: Текущее время
        start_position: Откуда
        end_position: Куда
        stations_list: Упорядоченный список станции
    return: 
        (Времня отбытия, Время окончания поездки, Кол-во станции)
    """
    # Получаем направление движения маршрута
    # В случае Обратного направления (вниз) реверсим stations_list
    descending_road =  stations_list.index(start_position) > stations_list.index(end_position) 
    if descending_road:
        stations_list = stations_list[::-1]
    # Получаем следующую станцию для нахождения времени отбытия
    next_station = stations_list[stations_list.index(start_position) + 1]
    mask = (
        (df['from'] == start_position)&
        (df['to'] == next_station)&
        (df['arrival_time'] > curr_time)
    )
    # Находим ближайщее время отбытия
    start_time = df[mask].iloc[0]['arrival_time']
    # Считаем количество секунд необходимое для преодоления маршрута после посадки
    # Время остановки и время пути небыло предоставленно
        # 5 * 60 по дефолту берем 5 минут на время между станциями
    add_seconds = (stations_list.index(end_position)  - stations_list.index(start_position) ) * 5 * 60
    # Суммируем со временем посадки
    end_time =  (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(seconds=add_seconds)).time()
    stations_count = stations_list.index(end_position)  - stations_list.index(start_position)
    return start_time, end_time, stations_count

if __name__ == "__main__":
    start_time, end_time, stations_count  = trip_duration(df, curr_time, start_position, end_position)

    print(f"Время отбытия: {start_time}")
    print(f"Время прибытия: {end_time}")
    print(f"Количество станции: {stations_count}")


