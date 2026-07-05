import pandas as pd
import pytest

from tests.constants import (
    INPUT_2_GROUPS_LEN,
    INPUT_DIR,
    INPUT_GENERAL_LEN,
    OUTPUT_DIR,
    PATTERN_GREEDY,
    PATTERN_MILP_2,
    PATTERN_MILP_G_2,
    PATTERN_MILP_G_GENERAL,
    PATTERN_MILP_GENERAL,
    PATTERN_MILP_SYM_2,
    PATTERN_MILP_SYM_GENERAL
)


@pytest.fixture
def input_dir():
    if INPUT_DIR.is_dir():
        return INPUT_DIR
    return False


@pytest.fixture
def output_dir():
    if OUTPUT_DIR.is_dir():
        return OUTPUT_DIR
    return False


@pytest.fixture
def input_files_2_groups(input_dir):
    if not input_dir:
        return []
    input_files_2_groups = [
        file for file in input_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and len(file.name) == INPUT_2_GROUPS_LEN
    ]
    return input_files_2_groups


@pytest.fixture
def input_files_general(input_dir):
    if not input_dir:
        return []
    input_files_general = [
        file for file in input_dir.iterdir()
        if file.is_file()
        and len(file.name) == INPUT_GENERAL_LEN
    ]
    return input_files_general


@pytest.fixture
def statistics(output_dir):
    if output_dir:
        for file in output_dir.iterdir():
            if file.is_file() and file.name.endswith('statistics.xlsx'):
                groups_2_stat = pd.read_excel(
                    file,  sheet_name='2 groups', index_col='instance'
                )
                general_stat = pd.read_excel(
                    file,  sheet_name='general', index_col='instance'
                )
                return general_stat, groups_2_stat
    return None, None


@pytest.fixture
def output_files_general_milp_g(output_dir):
    if not output_dir:
        return []
    output_files_general_milp_g = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_MILP_G_GENERAL.match(file.name)
    ]
    return output_files_general_milp_g


@pytest.fixture
def output_files_general_milp(output_dir):
    if not output_dir:
        return []
    output_files_general_milp = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_MILP_GENERAL.match(file.name)
    ]
    return output_files_general_milp


@pytest.fixture
def output_files_general_milp_s(output_dir):
    if not output_dir:
        return []
    output_files_general_milp_S = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_MILP_SYM_GENERAL.match(file.name)
    ]
    return output_files_general_milp_S


@pytest.fixture
def output_files_2_milp(output_dir):
    if not output_dir:
        return []
    output_files_2_milp = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_MILP_2.match(file.name)
    ]
    return output_files_2_milp


@pytest.fixture
def output_files_2_milp_s(output_dir):
    if not output_dir:
        return []
    output_files_2_milp_s = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_MILP_SYM_2.match(file.name)
    ]
    return output_files_2_milp_s


@pytest.fixture
def output_files_2_milp_g(output_dir):
    if not output_dir:
        return []
    output_files_2_milp_g = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_MILP_G_2.match(file.name)
    ]
    return output_files_2_milp_g


@pytest.fixture
def output_files_2_greedy(output_dir):
    if not output_dir:
        return []
    output_files_2_greedy = [
        file for file in output_dir.iterdir()
        if file.is_file()
        and file.name.endswith('.xlsx')
        and PATTERN_GREEDY.match(file.name)
    ]
    return output_files_2_greedy
