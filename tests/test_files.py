from src.constants import (
    MILP_DENSITY_COL,
    MILP_G_DENSITY_COL,
    MILP_S_DENSITY_COL
)

pytest_plugins = [
    'fixtures.files',
]


def test_input_dir_exists(input_dir):
    assert input_dir, 'Directory /Input is not found.'


def test_output_dir_exists(output_dir):
    assert output_dir, 'Directory /Output is not found.'


def test_input_files(input_files_general, input_files_2_groups):
    assert len(input_files_general), (
        'There are not xlsx-files in /Input '
        'for general partitioning'
    )
    assert len(input_files_2_groups), (
        'There are not xlsx-files in /Input '
        'for partitioning into 2 groups'
    )


def _test_output_files_for_model(
    stat,
    instance,
    density_key,
    output_file,
    output_files,
):
    return (
        stat.loc[instance][density_key] == -1
        or stat.loc[instance][density_key] > -1
        and any(output_file == file.name for file in output_files)
    )


def test_statistics(
    output_dir
):
    assert (
        any(file.is_file() and file.name.endswith('statistics.xlsx')
            for file in output_dir.iterdir())
    ), 'There is no `statistics.xlsx` file in /Output directory.'


def test_output_files(
        statistics,
        input_files_general,
        input_files_2_groups,
        output_files_general_milp_s,
        output_files_general_milp,
        output_files_general_milp_g,
        output_files_2_milp_s,
        output_files_2_milp,
        output_files_2_milp_g,
        output_files_2_greedy,
):
    general_stat, groups_2_stat = statistics
    assert (
        general_stat is not None and groups_2_stat is not None
    ), 'File statistics.xlsx was not read.'

    for input_file in input_files_general:
        instance = input_file.name[:-5]

        milp_s_output_file = f'milp_s_{input_file.name}'
        assert _test_output_files_for_model(
            general_stat,
            instance,
            MILP_S_DENSITY_COL,
            milp_s_output_file,
            output_files_general_milp_s,
        ), f'There is no `{milp_s_output_file}` file in /Output directory.'

        milp_output_file = f'milp_{input_file.name}'
        assert _test_output_files_for_model(
            general_stat,
            instance,
            MILP_DENSITY_COL,
            milp_output_file,
            output_files_general_milp,
        ), f'There is no `{milp_output_file}` file in /Output directory.'

        milp_g_output_file = f'milp_g_{input_file.name}'
        assert _test_output_files_for_model(
            general_stat,
            instance,
            MILP_G_DENSITY_COL,
            milp_g_output_file,
            output_files_general_milp_g,
        ), f'There is no `{milp_g_output_file}` file in /Output directory.'

    for input_file in input_files_2_groups:
        instance = input_file.name[:-5]

        milp_s_output_file = f'milp_s_{input_file.name}'
        assert _test_output_files_for_model(
            groups_2_stat,
            instance,
            MILP_S_DENSITY_COL,
            milp_s_output_file,
            output_files_2_milp_s,
        ), f'There is no `{milp_s_output_file}` file in /Output directory.'

        milp_output_file = f'milp_{input_file.name}'
        assert _test_output_files_for_model(
            groups_2_stat,
            instance,
            MILP_DENSITY_COL,
            milp_output_file,
            output_files_2_milp,
        ), f'There is no `{milp_output_file}` file in /Output directory.'

        milp_g_output_file = f'milp_g_{input_file.name}'
        assert _test_output_files_for_model(
            groups_2_stat,
            instance,
            MILP_G_DENSITY_COL,
            milp_g_output_file,
            output_files_2_milp_g,
        ), f'There is no `{milp_g_output_file}` file in /Output directory.'

        greedy_file = f'greedy_{input_file.name}'
        assert (
            greedy_file not in output_files_2_greedy
        ), f'There is no `{greedy_file}` file in /Output directory.'
