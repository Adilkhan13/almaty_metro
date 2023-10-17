import pandas as pd
import datetime

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
curr_time = datetime.datetime.today().time()
start_position = 'MSK'
end_position = 'SRN'
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
    add_seconds = (stations_list.index(end_position)  - stations_list.index(start_position) ) * 5 * 60
    # Суммируем со временем посадки
    end_time =  (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(seconds=add_seconds)).time()
    stations_count = stations_list.index(end_position)  - stations_list.index(start_position)
    return start_time, end_time, stations_count

start_time, end_time, stations_count  = trip_duration(df, curr_time, start_position, end_position)

print(f"Время отбытия: {start_time}")
print(f"Время прибытия: {end_time}")
print(f"Количество станции: {stations_count}")


