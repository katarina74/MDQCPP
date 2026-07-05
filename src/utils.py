from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from pyscipopt import Model, Variable


def get_edges_by_partition(
        partition: Union[List[List[int]], NDArray[np.int64]]
) -> List[Tuple[int, int]]:
    return [(partition[n][i], j) for n in range(len(partition))
            for i in range(len(partition[n])) for j in partition[n][i + 1:]]


def get_min_density_by_eddes(
        old_partition: Union[List[List[int]], NDArray[np.int64]],
        new_partition: Union[List[List[int]], NDArray[np.int64]],
) -> float:
    edges = get_edges_by_partition(old_partition)
    return min(
        2 * len([(new_partition[k][i], j) for i in range(len(new_partition[k]))
                 for j in new_partition[k][i + 1:]
                 if (new_partition[k][i], j) in edges])
        / (len(new_partition[k]) * (len(new_partition[k]) - 1))
        for k in range(len(new_partition))
    )


def get_group_sizes(
        lower_bound: int,
        upper_bound: int,
        num_of_students: int,
        num_of_new_groups: int,
) -> Tuple[int, int]:
    return (
        max(num_of_students - upper_bound * (num_of_new_groups - 1),
            lower_bound),
        min(num_of_students - lower_bound * (num_of_new_groups - 1),
            upper_bound)
    )


def get_sum_of_squares(
        quasi_clique_sizes: Union[List[List[int]], NDArray[np.int64]]
) -> int:
    return sum(i ** 2 for i in quasi_clique_sizes)


def get_density_by_sizes(
        quasi_clique_sizes: Union[List[List[int]], NDArray[np.int64]]
) -> float:
    size = sum(quasi_clique_sizes)
    return (
        get_sum_of_squares(quasi_clique_sizes)
        - size
    ) / (size * (size - 1))


def get_min_density_by_sizes(
        partition_sizes: Union[List[List[int]], NDArray[np.int64]]
) -> float:
    return (
        min(
            get_density_by_sizes(quasi_clique_sizes)
            for quasi_clique_sizes in partition_sizes
        )
    )


def _update_partitions(
    old_partition: List[List[int]],
    new_partition: List[List[int]],
    index_from: int,
    index_to: int,
    size: int,
) -> Tuple[List[int], List[int]]:
    return (
        new_partition[index_to] + list(old_partition[index_from][:size]),
        old_partition[index_from][size:]
    )


def get_partition_by_sizes(
    partition_sizes: List[List[int]],
    old_partition: List[List[int]]
) -> List[List[int]]:
    old_partition = deepcopy(old_partition)
    partition = [[] for _ in range(len(partition_sizes))]
    for k, sizes in enumerate(partition_sizes):
        for i, size in enumerate(sizes):
            partition[k], old_partition[i] = _update_partitions(
                old_partition,
                partition,
                i,
                k,
                size
            )
    return partition


def get_partition_by_sizes_sol(
        old_partition: List[List[int]],
        num_of_new_groups: int,
        variables: Dict[Tuple[int, int, int], Variable],
        model: Model,
        bynary_repr_q: Optional[bool] = False,
) -> List[List[int]]:
    partition = [[] for _ in range(num_of_new_groups)]
    old_partition = deepcopy(old_partition)
    if bynary_repr_q:
        for (k, i, s), var in variables.items():
            if round(model.getVal(var)):
                partition[k], old_partition[i] = _update_partitions(
                    old_partition,
                    partition,
                    i,
                    k,
                    s
                )
    else:
        for (k, i), var in variables.items():
            partition[k], old_partition[i] = _update_partitions(
                old_partition,
                partition,
                i,
                k,
                round(round(model.getVal(var)))
            )
    return partition
