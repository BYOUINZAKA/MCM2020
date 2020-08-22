from data import *
from typing import Iterable
from pandas import concat, DataFrame

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

    global trans_dict
    for name, group in df.groupby('Type'):
        print(f"{trans_dict[name]} :\t{func(df, name)}天")
    print()


def accumulate(time_list: Iterable, func=lambda x: x):
    value = func(time_list[0][1])
    current = time_list[0][0]

    for date, status in time_list[1:]:
        if current != date:
            yield value, current
            current = date
        value = value + func(status)

    yield value, current


def every(time_list: Iterable):
    value = abs(time_list[0][1])
    current = time_list[0][0]

    for date, status in time_list[1:]:
        if current != date:
            yield value, current
            current, value = date, 0
        value = value + abs(status)

    yield value, current

df = read_datas('plan')

invoke_print(df, "平均观察期", avgtime_observe)
invoke_print(df, "平均住院天数", avgtime_live)
invoke_print(df, "平均等待天数", avgtime_wait)

print("平均病床")
for group in df.groupby('Type'):
    time_list = get_time_list(group[1])

    sumval, count = 0, 0
    for hold, date in accumulate(time_list):
        sumval = sumval + hold
        count = count + 1

    print(f"{trans_dict[group[0]]} :\t{sumval/count}")

print()

print("平均周转")
for group in df.groupby('Type'):
    time_list = get_time_list(group[1])

    sumval, count = 0, 0
    for hold, date in every(time_list):
        sumval = sumval + hold
        count = count + 1

    print(f"{trans_dict[group[0]]} :\t{sumval/count}")