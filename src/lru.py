from collections import OrderedDict

# lru = least recently used
# evict the item whose most recent access time is the oldest

def lru_policy(k, m, r): 
    
    the_cache = OrderedDict()
    num_misses = 0
    

    for req in r: 
        
        if req in the_cache: 
            the_cache.move_to_end(req)
        else: 
            num_misses += 1
            if len(the_cache) == k:
                the_cache.popitem(last=False)
            the_cache[req] = True

    return num_misses