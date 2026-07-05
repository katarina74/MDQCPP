import pytest

from src.constants import (
    GREEDY_DENSITY_COL,
    MILP_DENSITY_COL,
    MILP_G_DENSITY_COL,
    MILP_S_DENSITY_COL
)
from src.data_processing import SolutionReader
from src.utils import get_min_density_by_sizes
from tests.constants import EPS
from tests.test_files import (test_input_dir_exists, test_input_files,  # noqa
                              test_output_dir_exists, test_output_files)

pytest_plugins = [
    'fixtures.files',
]


@pytest.mark.depends(on=["test_input_dir_exists",
                         "test_output_dir_exists",
                         "test_input_files",
                         "test_output_files"],)
def test_density_of_solutions(
    input_dir,
    output_files_general_milp_s,
    output_files_general_milp,
    output_files_general_milp_g,
    output_files_2_milp_s,
    output_files_2_milp,
    output_files_2_milp_g,
    output_files_2_greedy,
    statistics,
):
    general_stat, groups_2_stat = statistics

    for output_file in output_files_general_milp_s:
        solution = SolutionReader(
            input_dir / output_file.name[-10:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            general_stat.loc[output_file.name[-10:-5]]
            [MILP_S_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-10:-5]}` '
            'in statistics differs from real density '
            'for milp + symmetries breaking.')

    for output_file in output_files_general_milp:
        solution = SolutionReader(
            input_dir / output_file.name[-10:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            general_stat.loc[output_file.name[-10:-5]]
            [MILP_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-10:-5]}` '
            'in statistics differs from real density for milp.')

    for output_file in output_files_general_milp_g:
        solution = SolutionReader(
            input_dir / output_file.name[-10:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            general_stat.loc[output_file.name[-10:-5]]
            [MILP_G_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-10:-5]}` '
            'in statistics differs from real density for general milp.')

    for output_file in output_files_2_milp_s:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            groups_2_stat.loc[output_file.name[-12:-5]]
            [MILP_S_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-12:-5]}` '
            'in statistics differs from real density '
            'for milp + symmetries breaking.')

    for output_file in output_files_2_milp:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            groups_2_stat.loc[output_file.name[-12:-5]]
            [MILP_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-12:-5]}` '
            'in statistics differs from real density for milp.')

    for output_file in output_files_2_milp_g:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            groups_2_stat.loc[output_file.name[-12:-5]]
            [MILP_G_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-12:-5]}` '
            'in statistics differs from real density for general milp.')

    for output_file in output_files_2_greedy:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        real_density = get_min_density_by_sizes(solution.sol_partition_sizes)
        stat_density = (
            groups_2_stat.loc[output_file.name[-12:-5]]
            [GREEDY_DENSITY_COL]
        )
        assert (
            stat_density == -1
            or stat_density <= real_density
            or abs(real_density - stat_density) < EPS
        ), (f'Minimal density of solution `{output_file.name[-12:-5]}` '
            'in statistics differs from real density for greedy algorithm.')
