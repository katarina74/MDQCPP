import logging
from typing import List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from pyscipopt import Model

from src.constants import BIG_M
from src.utils import get_group_sizes

logger = logging.getLogger(__name__)


def run_milp_general_model(
        students: NDArray[np.int64],
        num_of_new_groups: int,
        lower_bound: int,
        upper_bound: int,
        edges: List[Tuple[int, int]],
        timelimit: Optional[Union[int, float]] = 10,
) -> Union[Tuple[float, List[List[int]]], Tuple[None, None]]:
    """
    MILP model. Divides a general graph into quasi-cliques.

    Args:
        students (NDArray[np.int64]): array of vertices
            (students in application)
        num_of_new_groups (int): number of creating quasi-cliques
        lower_bound (int): lower bound of size of each quasi-clique
        upper_bound (int): upper bound of size of each quasi-clique
        edges: (List[Tuple[int, int]]): edges of a given graph
        timelimit: Optional[Union[int, float]]: time limit
            for solving an optimization problems

    Returns:
        Union[Tuple[float, List[List[int]]], Tuple[None, None]]:
        minimal density and partition
        (list of lists, where each sublist means vertices of quasi-clique)
        or (None, None) if a feasible solution was not found
    """
    logger.info("Creating a model.")
    model = Model()

    x_vars = {
        (s, k): model.addVar(
            f'x{s}_{k}',
            vtype="B",
          )
        for s in students for k in range(num_of_new_groups)
    }

    lower_bound, upper_bound = get_group_sizes(
        lower_bound,
        upper_bound,
        len(students),
        num_of_new_groups
    )

    z_vars = {
        (k, size): model.addVar(
            f'x{k}_{size}',
            vtype="B",
          )
        for k in range(num_of_new_groups)
        for size in range(lower_bound, upper_bound + 1)
    }

    o_vars = {
        (k, u, v): model.addVar(
            f'x{k}_{u}_{v}',
            vtype="B",
        )
        for k in range(num_of_new_groups) for u, v in edges
    }

    gamma = model.addVar('gamma', 'C', lb=0, ub=1)

    model.setObjective(gamma, 'maximize')

    for s in students:
        model.addCons(sum(x_vars[s, k] for k in range(num_of_new_groups)) == 1)

    for k in range(num_of_new_groups):
        model.addCons(
            sum(x_vars[s, k] for s in students)
            == sum(size * z_vars[k, size] for size
                   in range(lower_bound, upper_bound + 1))
        )

    for k in range(num_of_new_groups):
        model.addCons(
            sum(z_vars[k, size] for size in
                range(lower_bound, upper_bound + 1)) == 1
        )

    for k in range(num_of_new_groups):
        for u, v in edges:
            model.addCons(o_vars[k, u, v] <= x_vars[u, k])
            model.addCons(o_vars[k, u, v] <= x_vars[v, k])

    for k in range(num_of_new_groups):
        for size in range(lower_bound, upper_bound + 1):
            model.addCons(
                sum(o_vars[k, u, v] for u, v in edges) >=
                gamma * size * (size - 1) / 2 - BIG_M * (1 - z_vars[k, size])
            )

    model.setParam("limits/time", timelimit)
    logger.info("Start optimizing.")
    model.optimize()
    logger.info("Finish optimizing.")

    if model.getNBestSolsFound():
        gamma_value = model.getVal(gamma)
        partition = [[] for _ in range(num_of_new_groups)]
        for (s, k), var in x_vars.items():
            if round(model.getVal(var)):
                partition[k].append(s)
        logger.info(f'Minimal density is {gamma_value:.10f}.')

        return gamma_value, partition

    logger.info("Solution was not found.")
    return None, None
