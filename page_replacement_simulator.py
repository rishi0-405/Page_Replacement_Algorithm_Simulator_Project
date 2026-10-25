# Page Replacement Algorithm Simulator
# Operating Systems Lab | Virtual Memory / Page Replacement
# Language: Python 3 (Jupyter Notebook)

from typing import List, Dict, Any, Tuple
import pandas as pd

def parse_reference_string(text: str) -> List[int]:
    """Parse comma- or whitespace-separated non-negative integer page numbers."""
    if not text or not text.strip():
        raise ValueError("Enter at least one page number.")
    tokens = text.replace(",", " ").split()
    pages = []
    for token in tokens:
        try:
            page = int(token)
        except ValueError:
            raise ValueError(
                "Page references must be whole numbers separated by commas or spaces."
            )
        if page < 0:
            raise ValueError("Page numbers must be non-negative integers.")
        pages.append(page)
    if not pages:
        raise ValueError("Enter at least one page number.")
    return pages

def simulate(reference: List[int], num_frames: int, algorithm: str) -> Tuple[int, int, List[Dict[str, Any]]]:
    """
    Simulate FIFO, LRU, or Optimal page replacement.
    Returns (page_faults, page_hits, trace).
    Trace frame lists use stable slot order. Empty slots are shown as '-'.
    """
    if not reference:
        raise ValueError("Reference string must contain at least one page.")
    if not isinstance(num_frames, int) or num_frames < 1:
        raise ValueError("Number of frames must be a whole number at least 1.")
    if any(not isinstance(p, int) or p < 0 for p in reference):
        raise ValueError("Page numbers must be non-negative integers.")

    policy = algorithm.strip().lower()
    if policy not in {"fifo", "lru", "optimal"}:
        raise ValueError("Algorithm must be FIFO, LRU, or Optimal.")

    frames = []
    arrival_order = []
    last_used = {}
    faults = 0
    hits = 0
    trace = []

    for i, page in enumerate(reference):
        replaced = "-"
        if page in frames:
            result = "H"
            hits += 1
            last_used[page] = i
        else:
            result = "F"
            faults += 1
            if len(frames) < num_frames:
                frames.append(page)
                arrival_order.append(page)
            else:
                if policy == "fifo":
                    victim = arrival_order.pop(0)
                elif policy == "lru":
                    victim = min(frames, key=lambda p: last_used[p])
                else:  # Optimal
                    future = reference[i + 1:]
                    distances = {}
                    for resident in frames:
                        try:
                            distances[resident] = future.index(resident)
                        except ValueError:
                            distances[resident] = float("inf")
                    # max() keeps the first frame on ties, including never-used-again pages.
                    victim = max(frames, key=lambda p: distances[p])
                replaced = victim
                slot = frames.index(victim)
                frames[slot] = page
                if policy == "fifo":
                    arrival_order.append(page)
                elif policy == "optimal":
                    pass
            last_used[page] = i

        # On FIFO, arrival_order is maintained independently of slot order.
        trace.append({
            "step": i + 1,
            "page": page,
            "frames": frames.copy(),
            "result": result,
            "replaced": replaced
        })

    return faults, hits, trace

def fifo(reference: List[int], num_frames: int):
    """FIFO wrapper; returns faults, hits and step-by-step trace."""
    return simulate(reference, num_frames, "fifo")

def lru(reference: List[int], num_frames: int):
    """LRU wrapper; returns faults, hits and step-by-step trace."""
    return simulate(reference, num_frames, "lru")

def optimal(reference: List[int], num_frames: int):
    """Optimal wrapper; returns faults, hits and step-by-step trace."""
    return simulate(reference, num_frames, "optimal")

def print_trace(reference: List[int], num_frames: int, algorithm: str) -> Dict[str, Any]:
    """Print a formatted trace and summary; return its metrics."""
    faults, hits, trace = simulate(reference, num_frames, algorithm)
    total = len(reference)
    print(f"\n{'=' * 18} {algorithm.upper()} {'=' * 18}")
    headers = ["Step", "Page", "Frame contents", "H/F", "Replaced"]
    rows = []
    for item in trace:
        frame_text = "[" + ", ".join(str(x) for x in item["frames"]) + "]"
        rows.append([item["step"], item["page"], frame_text, item["result"], item["replaced"]])
    display(pd.DataFrame(rows, columns=headers))
    print(f"Page faults : {faults}")
    print(f"Page hits   : {hits}")
    print(f"Hit ratio   : {hits / total:.2%}")
    print(f"Fault ratio : {faults / total:.2%}")
    return {
        "Algorithm": algorithm.upper(),
        "Page Faults": faults,
        "Page Hits": hits,
        "Hit Ratio": hits / total,
        "Fault Ratio": faults / total
    }

def compare_algorithms(reference: List[int], num_frames: int) -> pd.DataFrame:
    """Run all algorithms on identical input and display a comparison."""
    summaries = []
    for name in ("FIFO", "LRU", "Optimal"):
        summaries.append(print_trace(reference, num_frames, name))
    comparison = pd.DataFrame(summaries)
    comparison["Hit Ratio"] = comparison["Hit Ratio"].map(lambda x: f"{x:.2%}")
    comparison["Fault Ratio"] = comparison["Fault Ratio"].map(lambda x: f"{x:.2%}")
    print("\nFINAL PERFORMANCE COMPARISON")
    display(comparison)
    return comparison


if __name__ == "__main__":
    try:
        raw_reference = input("Enter page reference string: ")
        reference = parse_reference_string(raw_reference)
        raw_frames = input("Enter number of frames: ")
        try:
            num_frames = int(raw_frames)
        except ValueError:
            raise ValueError("Number of frames must be a whole number.")
        if num_frames < 1:
            raise ValueError("Number of frames must be at least 1.")
        compare_algorithms(reference, num_frames)
    except ValueError as error:
        print("Input error:", error)
