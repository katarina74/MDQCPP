from typing import List, Optional, Union

import numpy as np
from numpy.typing import NDArray


def _get_sizes_of_quasi_clique(
        cliques_sizes: NDArray[np.int64],
        number_of_cliques: int,
        number_of_vertices_in_quasi_clique: int,
        even_q: Optional[bool] = True,
) -> NDArray[np.int64]:
    quasi_clique = np.copy(cliques_sizes)
    quasi_clique[np.arange(even_q, number_of_cliques-1, 2)] = 0
    quasi_clique[-1] = (
        number_of_vertices_in_quasi_clique - sum(quasi_clique[:-1])
    )
    return quasi_clique


def get_partition_sizes_by_sizes_of_cliques(
        cliques_sizes: Union[List[int], NDArray[np.int64]]
) -> List[NDArray[np.int64]]:
    """
    Calculate a partition into 2 groups by greedy algorithm.

    Args:
        cliques_sizes (Union[List[int], NDArray[np.int64]]): Sizes of cliques

    Returns:
        List[List[int]]: List of lists.
            Means number of vertices taken from each
            clique into a current quasi-clique.

    Example:
        >>> get_partition_sizes_by_sizes_of_cliques([10, 10, 20])
        [array([10,  0, 10]), array([ 0, 10, 10])]
    """
    cliques_sizes_indexes = sorted(
        [(cs, i) for i, cs in enumerate(cliques_sizes)],
        key=lambda x: x[0]
    )
    cliques_sizes = np.array([cs for cs, _ in cliques_sizes_indexes])
    indexes = np.array([i for _, i in cliques_sizes_indexes])
    number_of_vertices_in_quasi_clique = int(sum(cliques_sizes) / 2)
    number_of_cliques = len(cliques_sizes)

    inverse = np.argsort(indexes)

    return [
        _get_sizes_of_quasi_clique(
            cliques_sizes,
            number_of_cliques,
            number_of_vertices_in_quasi_clique,
            even_q=True,
        )[inverse],
        _get_sizes_of_quasi_clique(
            cliques_sizes,
            number_of_cliques,
            number_of_vertices_in_quasi_clique,
            even_q=False,
        )[inverse]
    ]
