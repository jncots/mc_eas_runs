import multiprocessing
from tqdm import tqdm
from random import random


       
def my_func(arg):
    time.sleep(3*random())
    print(f"Proc_{arg}")
    return arg



if __name__ == '__main__':
    import time
    args = [i for i in range(50)]
    
    start = time.time()
    results = []
    with multiprocessing.Pool() as pool:
        for result in tqdm(pool.imap_unordered(my_func, args), 
                           total=len(args)):
            results.append(result)
    
    end = time.time()
    print(f"Elapsed time = {end - start}")