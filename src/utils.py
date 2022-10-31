import multiprocessing


def parallelize(threads_number, function, args, chunksize=None):
    pool = multiprocessing.Pool(threads_number)
    results = pool.starmap(function, args, chunksize=chunksize)
    pool.close()
    pool.join()
    return results
