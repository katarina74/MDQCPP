
import pytest

from src.data_processing import SolutionReader
from tests.test_files import (test_input_dir_exists, test_input_files,  # noqa
                              test_output_dir_exists, test_output_files)

pytest_plugins = [
    'fixtures.files',
]


@pytest.mark.depends(on=["test_input_dir_exists",
                         "test_output_dir_exists",
                         "test_input_files",
                         "test_output_files",])
def test_feasibility_of_solutions(
    input_dir,
    output_files_general_milp_s,
    output_files_general_milp,
    output_files_general_milp_g,
    output_files_2_milp_s,
    output_files_2_milp,
    output_files_2_milp_g,
    output_files_2_greedy,
):
    for output_file in output_files_general_milp_s:
        solution = SolutionReader(
            input_dir / output_file.name[-10:],
            output_file,
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-10:-5]}` '
            'for milp + symmetries breaking')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-10:-5]}` '
            'for milp + symmetries breaking')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-10:-5]}` '
                'for milp + symmetries breaking')

    for output_file in output_files_general_milp:
        solution = SolutionReader(
            input_dir / output_file.name[-10:],
            output_file,
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-10:-5]}` '
            'for milp')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-10:-5]}` '
            'for milp')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-10:-5]}` '
                'for milp')

    for output_file in output_files_general_milp_g:
        solution = SolutionReader(
            input_dir / output_file.name[-10:],
            output_file
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-10:-5]}` '
            'for general milp')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-10:-5]}` '
            'for general milp')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-10:-5]}` '
                'for general milp')

    for output_file in output_files_2_milp_s:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file,
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-12:-5]}` '
            'for milp + symmetries breaking')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-12:-5]}` '
            'for milp + symmetries breaking')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-12:-5]}` '
                'for milp + symmetries breaking')

    for output_file in output_files_2_milp:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-12:-5]}` '
            'for milp')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-12:-5]}` '
            'for milp')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-12:-5]}` '
                'for milp')

    for output_file in output_files_2_milp_g:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-12:-5]}` '
            'for general milp')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-12:-5]}` '
            'for general milp')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-12:-5]}` '
                'for general milp')

    for output_file in output_files_2_greedy:
        solution = SolutionReader(
            input_dir / output_file.name[-12:],
            output_file
        )
        assert (
            len(solution.data.students) == len(solution.students)
        ), ('Number of students in solution differs from '
            f'number of students in initial data `{output_file.name[-12:-5]}` '
            'for greedy algorithm')
        assert (
            (
                solution.data.number_of_quasi_cliques
                == len(solution.sol_partition)
            )
        ), ('Number of groups in solution differs from '
            f'number of groups in initial data `{output_file.name[-12:-5]}` '
            'for greedy algorithm')
        for qc in solution.sol_partition:
            qc_len = len(qc)
            assert (
                solution.data.lower_bound <= qc_len
                and qc_len <= solution.data.upper_bound
            ), ('Sizes of groups do not satisfy the boundaries '
                f'for initial data `{output_file.name[-12:-5]}` '
                'for greedy algorithm')
