import lru
import fifo
import optff

import sys


if __name__ == "__main__": 

    if len(sys.argv) != 3:
        print("Expected: python src/main.py <file_name.in> <file_name.out>")
        sys.exit()

    file = open(f'data/{sys.argv[1]}', 'r')

    cache_capacity, num_req = file.readline().split()

    reqs = file.readline().split()

    # k = cache capacity, m = number of requests, reqs = list of requests
    lru_misses = lru.lru_policy(cache_capacity, num_req, reqs)
    fifo_misses = fifo.fifo_policy(cache_capacity, num_req, reqs)
    optff_misses = optff.optff_policy(cache_capacity, num_req, reqs)

    file.close()
    output = open(f'data/{sys.argv[2]}', 'w')
    output.write(f"FIFO  : {fifo_misses}\n")
    output.write(f"LRU   : {fifo_misses}\n")
    output.write(f"OPTFF : {optff_misses}")
    output.close()



