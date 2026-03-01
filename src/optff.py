
# belady's farthest-in-future, optimal offline
# among items currently in the cache, evict the one whose next request occurs farthest in the future (or never occurs again)

def optff_policy(k, m, r): 
    print("optff")