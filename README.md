# MDQCPP
Algorithms for solving the Maximum Density Quasi-Clique Partition Problem

## Overview

Consider a cluster graph partitioning into $K$ quasi-cliques, where each subgraph has density at least $\gamma$ and order in given boundaries. The problem is to find a partition maximizing the value of $\gamma$. This project provides a set of optimization models and greedy hueristic for solving this problem. The main application of this problem is redistribution of second-year students at university into new academic groups by information of their belonging to previous groups.

The project supports four different approaches, ranging from exact Mixed-Integer Programming (MIP) to a fast greedy heuristic:

1.  **MILP with Symmetry Breaking (MILP-S):** A Mixed-Integer Linear Programming model for a cluster graph that includes constraints to break symmetries.
2.  **MILP without Symmetry Breaking (MILP):** A Mixed-Integer Linear Programming model for a cluster graph.
3.  **General MILP (MILP-G):** A general MILP model that works with arbitrary graph edges.
4.  **MINLP:** А Mixed Integer Nonlinear Programming model for a cluster graph.
5.  **MINQP:** А Mixed Integer Quadratic Programming model for a cluster graph.
6.  **Greedy Algorithm:** A fast heuristic for the special case of 2 groups, used as a benchmark.

The project reads input data from Excel files, runs the selected optimizations, logs the process, and compiles a comprehensive statistics report.

## Features

- **Multiple Optimization Models:** Compare exact and heuristic approaches for grouping.
- **Symmetry-Breaking Constraints:** Improves performance of the MILP model.
- **Greedy Algorithm:** Quick benchmark for the 2-group case.
- **Input/Output Handling:** Uses Excel (`.xlsx`) files for data ingestion and result storage.
- **Logging:** A detailed log file captures all solver outputs and performance metrics.
- **Statistics Generation:** Automatically compiles a final `statistics.xlsx` report comparing all models.
- **Time-Limited Solving:** All optimization models have a configurable time limit (default 3600 seconds).

## Project Structure

```text
.
├── Input/                      # Place your input .xlsx files here
├── Output/                     # Generated solution files and statistics are saved here
├── src/
│   ├── __init__.py             # Project-wide constants (directories, column names, etc.)
│   ├── constants.py            # Project-wide constants (directories, column names, etc.)
│   ├── data_processing.py      # DataReader, DataWriter, LogParser, and SolutionReader classes
│   ├── greedy_algorithm.py     # Implementation of the greedy algorithm for 2 groups
│   ├── milp.py                 # MILP model for cluster graph (with/without symmetry breaking)
│   ├── milp_general.py         # MILP model for general graphs
│   ├── minlp.py                # MINLP model (currently not used in main pipeline)
│   ├── miqp.py                 # MIQP model (currently not used in main pipeline)
│   └── utils.py                # Utility functions for partitions, densities, and graph operations
├── tests/                      # Test suite directory
│   ├── fixtures/               # Pytest fixtures directory
│   │   └── files.py            # Fixtures for file handling in tests
│   ├── conftest.py             # Pytest configuration and project root setup
│   ├── constants.py            # Test-specific constants (EPS, file patterns, etc.)
│   ├── test_density.py         # Tests validating density calculations in statistics
│   ├── test_feasibility.py     # Tests validating solution feasibility (sizes, counts)
│   └── test_files.py           # Tests validating input/output file existence and structure
├── log.log                     # Generated log file with all run details
├── flake8.txt                  # Flake8 configuration for code linting
├── gitignore.txt               # Git ignore rules (rename to .gitignore)
├── main.py                     # Main execution script
├── pytest.ini                  # Pytest configuration file
└── requirements.txt            # List of Python dependencies
```

## Requirements
You can install all dependencies using pip:
```pip install -r requirements.txt```
> **Note:** `pyscipopt` requires the SCIP Optimization Suite. If you are using a Linux/macOS system, you can install it via the package manager. Otherwise, please follow the official [PySCIPOpt installation guide](https://github.com/scipopt/PySCIPOpt#installation).

## Input Data Format

Each input Excel file (`.xlsx`) must contain two sheets:

### Sheet 1: `students`

| Student ID | Group |
| :--- | :--- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 2 |
| 5 | 2 |

- **Student ID:** The unique identifier for each student.
- **Group:** The ID of the original group (clique) the student belongs to.

### Sheet 2: `params`

| Parameter | Value |
| :--- | :--- |
| Lower Bound | 3 |
| Upper Bound | 5 |
| Number of Groups | 2 |

- **Lower Bound:** The minimum allowed size of any new group.
- **Upper Bound:** The maximum allowed size of any new group.
- **Number of Groups:** The desired number of groups to create (K).

## Usage
### Running the Main Script
Navigate to the project's root directory and run the main script:
```bash
python main.py
```

### Running Tests
To run the test suite and validate the correctness of the implementation:
```bash
pytest tests/
```
## Author 
Ekaterina Glazunova - katarina74

[katarina.glazunova97@inbox.ru](mailto:katarina.glazunova97@inbox.ru)
