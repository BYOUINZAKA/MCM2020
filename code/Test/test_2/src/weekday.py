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
