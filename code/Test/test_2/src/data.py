
import collections
import datetime
import heapq
import numpy as np

from datetime import timedelta
from typing import Iterable
from collections import namedtuple, deque
from pandas import DataFrame, read_csv, to_datetime

Case = collections.namedtuple(
    'Case', ['id', 'type', 'enter', 'standby', 'observe'])

MedicalMessage = namedtuple(
    'MedicalMessage', ['standby', 'observe', 'allow_days'])

trans_dict = {
    "Trauma": '外伤',
    "Retina": '视网膜疾病',
    "Glaucoma": '青光眼',
    "Cataract": '白内障',
    "Double": '白内障(双眼)',
}


def read_datas(sheet: str) -> DataFrame:
    return read_csv("code\\Test\\test_2\\%s.csv" % (sheet))


def duration(begin: str, end: str) -> int:
    if '/' in end:
        return np.Inf

    return (to_datetime(end) - to_datetime(begin)).days


def get_time_list(df: DataFrame):
    res = []
    for case in df.itertuples():
        res.append((to_datetime(case.In).date(), 1))
        try:
            res.append((to_datetime(case.Out).date(), -1))
        except:
            continue
    res.sort()
    return res


medical_dict = {
    "Trauma": MedicalMessage(1, 6, [0, 1, 2, 3, 4, 5, 6]),
    # "Retina": MedicalMessage(2, 10, [1, 3, 4, 5, 6]),
    # "Glaucoma": MedicalMessage(2, 8, [1, 3, 4, 5, 6]),
    "Retina": MedicalMessage(2, 10, [1, 3, 4]),
    "Glaucoma": MedicalMessage(2, 8, [1, 3, 4]),
    "Cataract": MedicalMessage(1, 3, [0, 2]),
    "Double": MedicalMessage(1, 5, [0]),
}


def weekday_advance(val, dis):
    res = val + dis
    if res > 6:
        return res - 7
    elif res < 0:
        return 7 + res
    else:
        return res


def weekday_distance(before, after):
    return after - before if before <= after else after + 7 - before


def find_suitable_day(date, msg: MedicalMessage):
    weekday = int(date.strftime("%w"))
    min_dis = 7

    for day in msg.allow_days:
        dis = weekday_distance(weekday, day)
        if dis >= msg.standby:
            min_dis = min(min_dis, dis)

    return (weekday, weekday_advance(weekday, min_dis)), min_dis


class TimeLine:
    def __init__(self, df) -> None:
        return self.load(df)

    def load(self, df: DataFrame):
        sdict = {}
        for case in df.itertuples():
            _in, _out = to_datetime(
                case.In).date(), to_datetime(case.Out).date()

            sdict.setdefault(_in, 0)
            sdict[_in] = sdict[_in] + 1

            sdict.setdefault(_out, 0)
            sdict[_out] = sdict[_out] - 1

        self.list = sorted(sdict.items())
        self.pointer, self.count = 0, 0

    def forward(self, target):
        try:
            target = to_datetime(target).date()
        except:
            pass
        base = self.pointer
        self.pointer = self.find(target)
        for i in range(base, self.pointer):
            self.count = self.count + self.list[i][1]

    def next(self, count=1):
        for i in range(self.pointer, self.pointer + count):
            self.count = self.count + self.list[i][1]

        self.pointer = self.pointer + count

    def has_next(self, count=1):
        return self.pointer + count < len(self.list)

    def find(self, target):
        slist = self.list
        for i in range(self.pointer, len(slist)):
            if slist[i][0] >= target:
                return i
        return len(slist)

    def input(self, out_time):
        try:
            out_time = to_datetime(out_time).date()
        except:
            pass

        self.modify(self.pointer, 1)

        out_index = self.find(out_time)

        if out_index < len(self.list) and self.list[out_index][0] == out_time:
            self.modify(out_index, -1)
        else:
            self.list.insert(out_index, (out_time, -1))

    def current(self):
        return (*self.list[self.pointer], self.count)

    def modify(self, idx: int, val: int):
        self.list[idx] = (self.list[idx][0], self.list[idx][1] + val)

    def __iter__(self):
        while True:
            yield self.current()
            if self.has_next():
                self.next()
            else:
                return

    def reset(self):
        self.pointer, self.count = 0, 0


def pop_case(case_heap: list, quick_queue: deque, today: datetime.date):
    if len(quick_queue) > 0:
        return 1, quick_queue.popleft()
    global medical_dict

    def allow(date_dis: int, standby: int):
        return date_dis >= standby

    date_dis, msg = heapq.heappop(case_heap)
    standby = medical_dict[msg[1]].standby
    while not allow(date_dis, standby):
        new_dis = find_suitable_day(today, medical_dict[msg[1]])[1]
        if new_dis > 7:
            print(new_dis)
        heapq.heappush(case_heap, (new_dis, msg))

        date_dis, msg = heapq.heappop(case_heap)
        standby = medical_dict[msg[1]].standby

    return date_dis, msg


def get_out_time(in_time: datetime.date, top: tuple):
    dis, msg = top
    observe = medical_dict[msg[1]].observe
    delta = timedelta(days=dis+observe)
    return in_time + delta

if __name__ == "__main__":
    forecast = read_datas('forecast_2')
    future = read_datas('future')

    time_line = TimeLine(forecast)
    case_heap = []
    quick_queue = deque(future[future['Type'] == 'Trauma'].to_numpy().tolist())

    time_line.forward("2008-9-12")
    today = time_line.current()[0]

    for msg in future[future['Type'] != 'Trauma'].to_numpy().tolist():
        dis = find_suitable_day(today, medical_dict[msg[1]])
        heapq.heappush(case_heap, (int(dis[1]), msg))

    def empty():
        return len(case_heap) + len(quick_queue) == 0

    plan = forecast.to_numpy()[:, 1:].tolist()
    double_delta = timedelta(days=2)

    for date, status, count in time_line:
        if empty():
            break

        beds, count = 79 - (count + status), 0

        while not empty() and count < beds:
            poped = pop_case(case_heap, quick_queue, date)
            out_date = get_out_time(date, poped)
            time_line.input(out_date)
            count = count + 1
            
            case = poped[1]
            wait = timedelta(days=poped[0])
            case[3] = date
            case[4] = date+wait
            if 'Double' == case[1]:
                case[-2] = case[-3] + double_delta
            case[-1] = out_date
            plan.append(case)
        
        for i in range(len(case_heap)):
            case_heap[i] = (case_heap[i][0]-1, case_heap[i][1])
    
    df = DataFrame(plan, columns=['ID','Type','Enter','In','First','Second','Out'])
    print(df)
    df.to_csv("code\\Test\\test_2\\plan_2.csv")