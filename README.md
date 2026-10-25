# Page Replacement Algorithm Simulator

An Operating Systems lab project that simulates **FIFO**, **LRU**, and **Optimal** page replacement in Python.

## Features
- Accepts comma- or space-separated page references and a frame count.
- Validates empty input, non-numeric pages, negative pages, and invalid frame counts.
- Displays step-by-step trace tables with step, page, frame contents, Hit/Fault, and replaced page.
- Calculates page faults, page hits, hit ratio, and fault ratio.
- Compares all three algorithms on the same input.
- Includes the assignment's manual tracing verification, Belady's anomaly experiment, custom inputs, and short answers.

## Files
- `Page_Replacement_Simulator.ipynb` — complete Jupyter Notebook with source code and demonstration cells.
- `Page_Replacement_Project_Report.pdf` — project report.
- `screenshots/` — sample execution screenshots.
- `LINKEDIN_POST.md` — professional project showcase post.

## Run locally
1. Install Python 3 and Jupyter Notebook.
2. Install pandas: `python -m pip install pandas notebook`
3. Open the notebook:
   ```bash
   jupyter notebook Page_Replacement_Simulator.ipynb
   ```
4. Run the cells in order. Use the interactive input cell to enter your own reference string and frame count.

## Algorithm summary
- **FIFO:** replaces the page loaded earliest.
- **LRU:** replaces the page that has not been used for the longest time in the past.
- **Optimal:** replaces the page whose next use is farthest in the future, or that will not be used again. It is a benchmark because future references are not available to a real OS.

## Metrics
- `Hit ratio = page hits / total page references`
- `Fault ratio = page faults / total page references`

## Reference
Operating Systems Lab Assignment — Page Replacement Algorithm Simulator; Silberschatz, Galvin and Gagne, *Operating System Concepts*.
