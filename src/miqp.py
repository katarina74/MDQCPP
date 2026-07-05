import logging
from typing import List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from pyscipopt import Model

from src.constants import BIG_M
from src.utils import get_group_sizes, get_partition_by_sizes_sol

logger = logging.getLogger(__name__)


def run_miqp_model(
        num_of_new_groups: int,
        num_of_old_groups: int,
        lower_bound: int,
        upper_bound: int,
        old_partition_num: List[int],
        old_partition: Union[List[List[int]], NDArray[np.int64]],
        timelimit: Optional[Union[int, float]] = 10
) -> Union[Tuple[float, List[List[int]]], Tuple[None, None]]:
    """
    MIQP Model. Divides a cluster graph into quasi-cliques.

    Args:
        students (NDArray[np.int64]): array of vertices
            (students in application)
        num_of_new_groups (int): number of creating quasi-cliques
        lower_bound (int): lower bound of size of each quasi-clique
        upper_bound (int): upper bound of size of each quasi-clique
        old_partition_num (List[int]): sizes of cliques
        old_partition: (Union[List[List[int]], NDArray[np.int64]]):
            list of lists, where each sublist is a clique
        timelimit (Optional[Union[int, float]]):
            time limit for solving an optimization problem

    Returns:
        Union[Tuple[float, List[List[int]]], Tuple[None, None]]:
            minimal density and partition
            (list of lists, where each sublist means vertices of quasi-clique)
            or (None, None) if a feasible solution was not found
    """
    logger.info("Creating a model.")
    model = Model()

    x_vars = {
        (k, n): model.addVar(
            f'x{k}_{n}',
            vtype="I",
            lb=0,
            ub=min(upper_bound, old_partition_num[n])
          )
        for n in range(num_of_old_groups)
        for k in range(num_of_new_groups)
      }
    z_vars = {
        (k, size):  model.addVar(
            f'z{k}_{size}',
            vtype="B",
          )
        for k in range(num_of_new_groups)
        for size in range(lower_bound, upper_bound + 1)
    }
    gamma = model.addVar('gamma', 'C', lb=0, ub=1)

    model.setObjective(gamma, 'maximize')

    lower_bound, upper_bound = get_group_sizes(
        lower_bound,
        upper_bound,
        sum(old_partition_num),
        num_of_new_groups
    )

    for k in range(num_of_new_groups):
        model.addCons(
            sum(x_vars[k, n] for n in range(num_of_old_groups))
            == sum(size * z_vars[k, size] for size in
                   range(lower_bound, upper_bound + 1))
        )

    for k in range(num_of_new_groups):
        model.addCons(
            sum(
                z_vars[k, size] for size
                in range(lower_bound, upper_bound + 1)
            ) == 1
        )

    for n in range(num_of_old_groups):
        model.addCons(
            sum(x_vars[k, n] for k in range(num_of_new_groups))
            == old_partition_num[n]
        )

    for k in range(num_of_new_groups):
        for size in range(lower_bound, upper_bound + 1):
            num_of_add_edges = sum(
                x_vars[k, n] * (x_vars[k, n] - 1)
                for n in range(num_of_old_groups - 1)
            )
            model.addCons(gamma <= num_of_add_edges / (size * (size - 1))
                          + BIG_M * (1 - z_vars[k, size]))

    model.setParam("limits/time", timelimit)
    logger.info("Start optimizing.")
    model.optimize()
    logger.info("Finish optimizing.")

    if model.getNBestSolsFound():
        gamma_value = model.getVal(gamma)
        partition = get_partition_by_sizes_sol(
            old_partition,
            num_of_new_groups,
            x_vars,
            model,
        )
        logger.info(f'Minimal density is {gamma_value:.10f}.')

        return gamma_value, partition

    logger.info("Solution was not found.")
    return None, None
