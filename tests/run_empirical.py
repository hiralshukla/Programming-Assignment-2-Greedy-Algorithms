# tests/run_empirical.py
from pathlib import Path
import subprocess
import sys

INPUT_FILES = ["file1.in", "file2.in", "file3.in"]

def parse_output_file(path: Path) -> dict:
    """
    Expects:
      FIFO  : <n>
      LRU   : <n>
      OPTFF : <n>
    Returns dict like {"FIFO": 9, "LRU": 10, "OPTFF": 7}
    """
    results = {}
    with path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            left, right = line.split(":")
            policy = left.strip()   # "FIFO", "LRU", "OPTFF"
            misses = int(right.strip())
            results[policy] = misses

    for key in ("FIFO", "LRU", "OPTFF"):
        if key not in results:
            raise ValueError(f"Missing {key} in output file: {path}")
    return results


def read_k_m(input_path: Path) -> tuple[int, int]:
    with input_path.open("r") as f:
        first = f.readline().strip()
    k, m = map(int, first.split())
    return k, m


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    src_main = repo_root / "src" / "main.py"

    if not src_main.exists():
        print("ERROR: src/main.py not found.")
        return 1

    rows = []

    for infile in INPUT_FILES:
        in_path = data_dir / infile
        if not in_path.exists():
            print(f"ERROR: missing input file: {in_path}")
            return 1

        k, m = read_k_m(in_path)

        # main.py expects just filenames and takes care of args
        out_name = infile.rsplit(".", 1)[0] + ".out"
        out_path = data_dir / out_name

        cmd = [sys.executable, str(src_main), infile, out_name]
        completed = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)

        if completed.returncode != 0:
            print(f"ERROR running: {' '.join(cmd)}")
            if completed.stdout:
                print("STDOUT:\n" + completed.stdout)
            if completed.stderr:
                print("STDERR:\n" + completed.stderr)
            return completed.returncode

        results = parse_output_file(out_path)
        rows.append((infile, k, m, results["FIFO"], results["LRU"], results["OPTFF"]))

    # Write the summary file used for Q1 in the README
    summary_path = data_dir / "q1_results.txt"
    with summary_path.open("w") as f:
        f.write("Input File\tk\tm\tFIFO\tLRU\tOPTFF\n")
        for (infile, k, m, fifo_m, lru_m, optff_m) in rows:
            f.write(f"{infile}\t{k}\t{m}\t{fifo_m}\t{lru_m}\t{optff_m}\n")

    print(f"Wrote: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())