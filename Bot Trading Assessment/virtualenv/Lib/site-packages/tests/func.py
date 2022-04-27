def memory(x):
    x = [i for i in range(x)]
    return -1


def time(x):
    # recursive function to find xth fibonacci number
    if x < 3:
        return 1
    return time(x-1) + time(x-2)


def error(x=None):
    # error function
    return "a" / 2


def return_check(*args, **kwagrs):
    # args and kwargs function
    return list(args) + list(kwagrs.values())
