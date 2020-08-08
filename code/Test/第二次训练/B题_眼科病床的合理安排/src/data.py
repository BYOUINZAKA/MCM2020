
import collections
from typing import Callable, Iterable
import numpy as np

from pandas import DataFrame, read_csv, to_datetime, concat

'''
病床利用率
等待时间

客观耗时：手术准备期、观察期
主观耗时：门诊期、手术日期
'''
Case = collections.namedtuple(
    'Case', ['id', 'type', 'enter', 'standby', 'observe'])


def read_datas(sheet: str) -> DataFrame:
    return read_csv("code\\Test\\第二次训练\\B题_眼科病床的合理安排\\%s.csv" % (sheet))


def duration(begin: str, end: str) -> int:
    if '/' in end:
        return np.Inf

    return (to_datetime(end) - to_datetime(begin)).days


def avgtime_observe(df: DataFrame, typename: str):
    is_double = 'Double' in typename
    group = df.groupby('Type').get_group(typename)
    sumval = 0
    for case in group.itertuples():
        sumval = sumval + \
            duration(case.Second if is_double else case.First, case.Out)
    return sumval / group.shape[0]


def avgtime_live(df: DataFrame, typename: str):
    group = df.groupby('Type').get_group(typename)
    sumval = 0
    for case in group.itertuples():
        sumval = sumval + duration(case.In, case.Out)
    return sumval / group.shape[0]


def avgtime_wait(df: DataFrame, typename: str):
    group = df.groupby('Type').get_group(typename)
    sumval = 0
    for case in group.itertuples():
        sumval = sumval + duration(case.Enter, case.In)
    return sumval / group.shape[0]


def invoke_print(df: DataFrame, title: str, func: callable):
    print(f"{title}: ")

    print(f"外伤：\t\t{func(df, 'Trauma')}天")
    print(f"视网膜疾病：\t{func(df, 'Retina')}天")
    print(f"青光眼：\t{func(df, 'Glaucoma')}天")
    print(f"白内障：\t{func(df, 'Cataract')}天")
    print(f"白内障(双眼)：\t{func(df, 'Double')}天\n")


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


def accumulate(time_list: Iterable, func=lambda x: x):
    value = func(time_list[0][1])
    current = time_list[0][0]

    for date, status in time_list[1:]:
        if current != date:
            yield value, current
            current = date
        value = value + func(status)

    yield value, current


if __name__ == "__main__":
    past = read_datas('past')
    curr = read_datas('current')

    df = concat([past, curr])

    '''
    invoke_print(past, "平均观察期", avgtime_observe)
    invoke_print(past, "平均住院天数", avgtime_live)
    invoke_print(past, "平均等待天数", avgtime_wait)
    '''

    time_list = get_time_list(df)

    for hold, date in accumulate(time_list):
        print(date, hold)
