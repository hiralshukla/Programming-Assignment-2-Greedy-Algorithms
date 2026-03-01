from collections import deque

# fifo = first in first out
# evict the item that has been in the cache the longest

def fifo_policy(k, m, r): 
    
    the_cache = set()
    queue = deque()
    num_misses = 0


    for req in r:
        if req in the_cache: 
            continue

        num_misses += 1

        if len(the_cache) == k:
            old = queue.popleft()
            the_cache.remove(old)
            
        the_cache.add(req)
        queue.append(req)

    return num_misses