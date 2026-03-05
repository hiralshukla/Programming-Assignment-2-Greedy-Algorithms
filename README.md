# Cache Eviction Policies Simulator (FIFO, LRU, OPTFF)

## Student Info

- Emily Apel UFID: 34845199
- Hiral Shukla UFID: 42066733

## Compile / Build

No compilation is required. This project uses **Python** and the standard library only.

## How to Run

`src/main.py` expects two command-line arguments:

1. input filename (located in `data/`)
2. output filename (to be created in `data/`)

Run from the repository root:

```bash
python src/main.py <input_file> <output_file>
```

Example:

```powershell
python3 src/main.py example.in example_run.out
```

## Assumptions

- Python is installed.
- Input files are stored in the `data/` folder.
- Output files are written to the `data/` folder.
- Input format:
    - First line: `k m`
    - Second line: exactly `m` integer request IDs (white space-separated).
- Requests are read from the **second line only** (the driver reads one line for the request sequence).
- Output format:
    - `FIFO : <misses>`
    - `LRU : <misses>`
    - `OPTFF : <misses>`

---

## Question 1: **Empirical Comparison**

*For each file, I am reporting the number of cache misses for each policy*

| Input File | k | m | FIFO | LRU | OPTFF |
| --- | --- | --- | --- | --- | --- |
| file1.in | 3 | 60 | 22 | 12 | 12 |
| file2.in | 4 | 80 | 50 | 48 | 38 |
| file3.in | 5 | 60 | 45 | 45 | 36 |

**Does OPTFF have the fewest misses?** 

Yes, because OPTFF knows the entire future request sequence and always evicts the item whose next use is farthest in the future (or never occurs again), minimizing misses.

**How does FIFO compare to LRU?**
FIFO usually has **more misses** than LRU on typical workloads because it ignores recency. 

FIFO can evict an item that was just used and is about to be used again simply because it was inserted earlier, while LRU uses recent access history to match temporal locality and therefore tends to have fewer misses and perform closer to OPTFF.

## Question 2: Bad Sequence for LRU or FIFO (k = 3)

Yes, such a sequence exists, for which OPTFF incurs strictly fewer misses than LRU (or FIFO).

Let `k = 3`, `m = 12`, and the request sequence be:
`1 2 3 4 1 2 5 1 2 3 4 5`

Miss counts:

- FIFO: 9 misses
- LRU: 10 misses
- OPTFF: 7 misses

Therefore, OPTFF incurs strictly fewer misses than both FIFO and LRU on this sequence (`7 < 9` and `7 < 10`) because FIFO and LRU are online policies that do not know future requests and can evict an item that will be needed soon, while OPTFF uses future knowledge to evict the item used farthest in the future.

## Question 3: **Prove OPTFF is Optimal**

Let OPTFF be Belady’s Farthest-in-Future algorithm.

For any request sequence and any offline algorithm A,

$$
misses(OPTFF)≤misses(A)
$$

### Proof

Among all optimal offline schedules, choose one schedule S that agrees with OPTFF for the longest prefix of requests.

Let $j$ be the first step where $S$ and OPTFF differ.

Since they behaved the same before step $j$, their cache contents are identical before request $r_{j}$

Let $d= r_{j}$

### Case 1: $d$ is already in the cache

Both algorithms have a **cache hit**.

No eviction occurs, so $S$ already agrees with OPTFF for step $j$.

Thus the invariant holds.

### Case 2: $d$ is not in the cache and both evict the same item

Both algorithms have a miss and evict the same item

They still behave the same, so the invariant holds

### Case 3: $d$ is not in the cache and they evict different items

Suppose

- OPTFF evicts item $e$
- S evicts item $f$, where $f \neq e$

Since OPTFF evicts the item used **farthest in the future**,

$$
next(e) \neq next(f)
$$

Construct a new schedule $S'$

- At step $j$, evict $e$ instead of $f$.

Now $S'$ agrees with OPTFF through step $j$

Let $j'$ be the first step after $j$ where $S'$ would behave differently from $S$.

Let $g$ be the request at step $j'$

### Case 3a: $g = e$

This cannot happen

Since OPTFF chose $e$ as the item requested farthest in the future, there must be a request for $f$  before $e$.

### Case 3b: $g = f$

Schedule $S$ must miss on $f$

Modify $S'$ so it evicts the same item that $S$ evicts

After this step the caches become identical again

### Case 3c: $q \neq e, f$

If $S$ evicts $e$, then make $S'$ evict $f$

After that the cache states again become identical

---

Thus we can construct a schedule $S'$ that

- is still optimal
- agrees with OPTFF for one more step

This contradicts the assumption that $S$ agreed with OPTFF for the longest prefix

Therefore OPTFF must be optimal, and

$$
misses(OPTFF)≤misses(A)
$$

for any offline algorithm A.
