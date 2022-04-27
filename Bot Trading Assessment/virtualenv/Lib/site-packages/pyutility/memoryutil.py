import sys
import tracemalloc as tm
import multiprocessing as mp

if sys.platform == "win32":
    from ._windows import resource
else:
    import resource


def me_worker(func, storage, *args, **kwargs):
    """measures the peak memory consumption of given function

    Args:
        func (`function`): function to execute
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        peak memory used during the execution of given function in bytes (`int`)
    """

    tm.start()
    now_mem, peak_mem = tm.get_traced_memory()

    value = func(*args, **kwargs)

    new_mem, new_peak = tm.get_traced_memory()
    tm.stop()

    storage.append(new_peak - now_mem)

    return new_peak - now_mem


def li_worker(func, limit, storage, *args, **kwargs):
    """limits the memory consumption of given function

    Args:
        func (`function`): function to execute
        limit (`int`): maximum allowed memory consumption
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or MemoryError
    """
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,
                       (int(limit * 1024 * 1024), hard))

    try:
        value = func(*args, **kwargs)
        storage.append(value)
    except Exception as error:
        storage.append(error)
    finally:
        resource.setrlimit(resource.RLIMIT_AS, (soft, hard))

    return 0


def memoryit(func, args=(), kwargs={}):
    """measures the peak memory consumption of given function

    Args:
        func (`function`): function to execute
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        peak memory used during the execution of given function in bytes (`int`)
    """
    ctx = mp.get_context('spawn')
    manager = ctx.Manager()
    com_obj = manager.list()
    p = ctx.Process(target=me_worker, args=(
        func, com_obj, *args), kwargs=kwargs)
    p.start()
    p.join()

    return com_obj[-1]


def limit_memory(func, memory=25, args=(), kwargs={}):
    """limits the memory consumption of given function. 
    If limit set is very low it will not behave in expected way.

    Args:
        func (`function`): function to execute
        limit (`int`): maximum allowed memory consumption in MB default is 25 MB
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or MemoryError
    """

    ctx = mp.get_context('spawn')
    manager = ctx.Manager()
    com_obj = manager.list()
    p = ctx.Process(target=li_worker, args=(
        func, memory, com_obj, *args), kwargs=kwargs)
    p.start()
    p.join()

    if isinstance(com_obj[-1], Exception):
        raise com_obj[-1]
    else:
        return com_obj[-1]
