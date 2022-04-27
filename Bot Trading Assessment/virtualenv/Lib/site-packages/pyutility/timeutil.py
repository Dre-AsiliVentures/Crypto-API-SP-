from time import time
import multiprocessing as mp


def me_worker(func, storage, *args, **kwargs):
    """measures the time taken to execute given function
    Args:
        func (`function`): function to execute
        storage (`list`): multiprocessing.Manager().List() to store the time taken to excute
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        time taken to execute the given function in seconds (`float`)
    """
    t1 = time()
    func(*args, **kwargs)
    t2 = time()
    storage.append(t2-t1)
    return t2 - t1


def li_worker(func, time, storage, *args, **kwargs):
    """limits the time taken for exection of given function

    Args:
        func (`function`): function to execute
        limit (`int`): maximum allowed time in seconds
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or TimeoutError
    """

    try:
        value = func(*args, **kwargs)
        storage.append(value)
    except Exception as error:
        storage.append(error)

    return 0


def timeit(func, args=(), kwargs={}):
    """measures the time taken to execute given function

    Args:
        func (`function`): function to execute
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        time taken to execute the given function in seconds (`float`)
    """

    ctx = mp.get_context('spawn')
    manager = ctx.Manager()
    com_obj = manager.list()
    p = ctx.Process(target=me_worker, args=(
        func, com_obj, *args), kwargs=kwargs)
    p.start()
    p.join()

    return com_obj[-1]


def limit_time(func, time=10, args=(), kwargs={}):
    """limits the time taken for exection of given function

    Args:
        func (`function`): function to execute
        limit (`int`): maximum allowed time in seconds, default is 10
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or TimeoutError
    """

    ctx = mp.get_context('spawn')
    manager = ctx.Manager()
    com_obj = manager.list()
    p = ctx.Process(target=li_worker, args=(
        func, time, com_obj, *args), kwargs=kwargs)
    p.start()
    p.join(time)
    
    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError

    if isinstance(com_obj[-1], Exception):
        raise com_obj[-1]
    else:
        return com_obj[-1]
