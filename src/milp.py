import logging
from typing import List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from pyscipopt import Model
from tabulate import tabulate

from src.constants import BIG_M
from src.utils import get_group_sizes, get_partition_by_sizes_sol

logger = logging.getLogger(__name__)


def run_milp_cliques_model(
        students: NDArray[np.int64],
        num_of_new_groups: int,
        lower_bound: int,
        upper_bound: int,
        old_partition_num: List[int],
        old_partition: Union[List[List[int]], NDArray[np.int64]],
        timelimit: Optional[Union[int, float]] = 10,
        break_symmetries_q: Optional[bool] = False
) -> Union[Tuple[float, List[List[int]]], Tuple[None, None]]:
    """
    MILP model. Divides a cluster graph into quasi-cliques.

    Args:
        students (NDArray[np.int64]):
            array of vertices (students in application)
        num_of_new_groups (int): number of creating quasi-cliques
        lower_bound (int): lower bound of size of each quasi-clique
        upper_bound (int): upper bound of size of each quasi-clique
        old_partition_num (List[int]): sizes of cliques
        old_partition: (Union[List[List[int]], NDArray[np.int64]]):
            list of lists, where each sublist is a clique
        timelimit (Optional[Union[int, float]]):
            time limit for solving an optimization problem
        break_symmetries_q (Optional[bool]):
            adds to a model symmetries-breaking constraints if True

    Returns:
        Union[Tuple[float, List[List[int]]], Tuple[None, None]]:
            minimal density and partition
            (list of lists, where each sublist means vertices of quasi-clique)
            or (None, None) if a feasible solution was not found
    """
    logger.info("Creating a model.")
    model = Model()

    x_vars = {
        (k, i, s): model.addVar(
            f'x{k}_{i}_{s}',
            vtype="B",
          )
        for k in range(num_of_new_groups)
        for i, n in enumerate(old_partition_num)
        for s in range(min(upper_bound + 1, n + 1))
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

    gamma = model.addVar('gamma', 'C', lb=0, ub=1)

    model.setObjective(gamma, 'maximize')

    for i, n in enumerate(old_partition_num):
        model.addCons(sum(s * x_vars[k, i, s] for k in range(num_of_new_groups)
                          for s in range(min(n + 1, upper_bound + 1))) == n)

    for k in range(num_of_new_groups):
        model.addCons(
            sum(
                s * x_vars[k, i, s] for i, n in
                enumerate(old_partition_num)
                for s in range(min(n + 1, upper_bound + 1))
            ) == sum(
                size * z_vars[k, size] for
                size in range(lower_bound, upper_bound + 1)
            )
        )

    for k in range(num_of_new_groups):
        model.addCons(
            sum(
                z_vars[k, size] for
                size in range(lower_bound, upper_bound + 1)
            ) == 1
        )

    for (k, size), z_var in z_vars.items():
        model.addCons(
            gamma <= sum(s * (s - 1) * x_vars[k, i, s] for
                         i, n in enumerate(old_partition_num)
                         for s in range(min(n + 1, upper_bound + 1))
                         ) / (size * (size - 1)) + BIG_M * (1 - z_var)
        )

    if break_symmetries_q:

        for k in range(num_of_new_groups):
            for i, n in enumerate(old_partition_num):
                model.addCons(
                    sum(
                        x_vars[k, i, s]
                        for s in range(min(n + 1, upper_bound + 1))
                    ) == 1
                )

        lex = {
            (k, i, s): model.addVar(f'lex{k}_{i}_{s}', vtype="B",)
            for k in range(num_of_new_groups - 1)
            for i, n in enumerate(old_partition_num)
            for s in range(min(n + 1, upper_bound + 1))
        }

        eq = {
            (k, i, s): model.addVar(f'eq{k}_{i}_{s}', vtype="B",)
            for k in range(num_of_new_groups - 1)
            for i, n in enumerate(old_partition_num)
            for s in range(min(n + 1, upper_bound + 1))
        }

        for k in range(num_of_new_groups - 1):
            for i, n in enumerate(old_partition_num):
                if i == 0:
                    model.addCons(x_vars[k, 0, 0] <= x_vars[k + 1, 0, 0])
                    model.addCons(lex[k, 0, 0] >= eq[k, 0, 0])
                else:
                    model.addCons(
                        x_vars[k, i, 0] <= x_vars[k + 1, i, 0] +
                        1 - lex[k, i - 1, min(old_partition_num[i - 1],
                                              upper_bound)]
                    )
                    model.addCons(
                        lex[k, i, 0] >= lex[k, i - 1,
                                            min(old_partition_num[i - 1],
                                                upper_bound)]
                        - (1 - eq[k, i, 0])
                    )

                    for s in range(0, min(n + 1, upper_bound + 1)):
                        model.addCons(
                            x_vars[k, i, s] + x_vars[k + 1, i, s] - 1
                            <= eq[k, i, s]
                        )
                        model.addCons(
                            1 - x_vars[k, i, s] - x_vars[k + 1, i, s]
                            <= eq[k, i, s]
                        )
                        if s > 0:
                            model.addCons(
                                x_vars[k, i, s] <= x_vars[k + 1, i, s]
                                + (1 - lex[k, i, s - 1])
                            )
                            model.addCons(
                                lex[k, i, s]
                                >= lex[k, i, s - 1] - (1 - eq[k, i, s])
                            )
                        else:
                            model.addCons(
                                x_vars[k, i, s] <= x_vars[k + 1, i, s] + 1
                            )
                            model.addCons(
                                lex[k, i, s] >= - 1 + eq[k, i, s]
                            )

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
            bynary_repr_q=True
        )
        logger.info(f'Minimal density is {gamma_value:.10f}.')

        # prints a list of lists, where each sublist corresponds
        # to a quasi-qlique. Each element of sublist is a number of
        # vertices taken from each clique to a current quasi-qlique
        if break_symmetries_q:
            num_of_verticies_in_quasi_cliques = []
            for k in range(num_of_new_groups):
                current_quasi_qlique = []
                for i, n in enumerate(old_partition_num):
                    for s in range(min(upper_bound + 1, n + 1)):
                        if round(model.getVal(x_vars[k, i, s])) == 1:
                            current_quasi_qlique.append(s)
                            break
                num_of_verticies_in_quasi_cliques.append(current_quasi_qlique)
            print(tabulate(num_of_verticies_in_quasi_cliques))

        return gamma_value, partition

    logger.info("Solution was not found.")
    return None, None
