from collections import deque

# belady's farthest-in-future, optimal offline
# among items currently in the cache, evict the one whose next request occurs farthest in the future (or never occurs again)

def optff_policy(k, m, r): 
    
    req_futures = {}

    for index, req in enumerate(r):
        if req not in req_futures:
            req_futures[req] = deque()
        req_futures[req].append(index)

    the_cache = set()
    num_misses = 0

    for req in r:

        req_futures[req].popleft()

        if req in the_cache:
            continue

        num_misses += 1

        if len(the_cache) == k:
            
            farthest_in_future_index = -1
            evicted = None

            for page in the_cache:
                if not req_futures[page]:
                    evicted = page
                    break

                next_use_index = req_futures[page][0]
                if next_use_index > farthest_in_future_index:
                    farthest_in_future_index = next_use_index
                    evicted = page

            the_cache.remove(evicted)

        the_cache.add(req)      

    return num_misses  