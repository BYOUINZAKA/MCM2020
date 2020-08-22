import heapq

from datetime import datetime, timedelta
from data import MedicalMessage, trans_dict, read_datas
from weekday import weekday_distance, weekday_advance
from pandas import DataFrame, to_datetime

medical_dict = {
    "Trauma": MedicalMessage(1, 6, [0, 1, 2, 3, 4, 5, 6]),
    "Retina": MedicalMessage(2, 10, [1, 3, 4, 5, 6]),
    "Glaucoma": MedicalMessage(2, 8, [1, 3, 4, 5, 6]),
    "Cataract": MedicalMessage(1, 3, [0, 2]),
    "Double": MedicalMessage(1, 5, [0]),
}


def find_suitable_day(date, msg: MedicalMessage):
    weekday = int(date.strftime("%w"))
    min_dis = 7

    for day in msg.allow_days:
        dis = weekday_distance(weekday, day)
        if dis >= msg.standby:
            min_dis = min(min_dis, dis)

    return (weekday, weekday_advance(weekday, min_dis)), min_dis


def build_forecast():
    delta_double = timedelta(days=medical_dict['Cataract'].observe)

    def forecast(df: DataFrame):
        if 'Double' in df['Type']:
            df['Out'] = to_datetime(df['Second']) + delta_double
        else:
            df['Out'] = to_datetime(
                df['First']) + timedelta(days=medical_dict[df['Type']].observe)
        return df

    curr = read_datas('current_2')
    forecast_datas = curr.apply(forecast, axis=1)
    print(forecast_datas)
    forecast_datas.to_csv("code\\Test\\test_2\\forecast_2.csv")


if __name__ == "__main__":
    build_forecast()
    pass
