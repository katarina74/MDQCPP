import re
from datetime import datetime
from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from src.constants import (
    COLUMNS_2_GROUPS,
    COLUMNS_GENERAL,
    DENSITY_PATTERN,
    FILE_NAME_PATTERN
)


class DataReader:
    """
    Reader for initial data.

    Attributes:
        students_df: DataFrame with data from sheet `students`.
        students: array of students.
        old_partition: list of lists.
            Each sublist means a group in initial partition.
        old_partition_num: size of each group in initial partition.
        lower_bound: lower bound of groups size.
        upper_bound: upper bound of groups size.
        number_of_quasi_cliques: number of creating groups.
    """

    def __init__(
            self,
            path_to_input_file: Union[str, Path]
    ) -> None:
        self.students_df = pd.read_excel(
            path_to_input_file,  sheet_name='students',
        )
        self.students = self.students_df['Student ID'].values
        self.old_partition = (
            self.students_df.groupby('Group')
            ['Student ID'].apply(list).tolist()
        )
        self.old_partition_num = [len(i) for i in self.old_partition]

        info_df = pd.read_excel(
            path_to_input_file, sheet_name='params', index_col='Parameter'
        )

        self.lower_bound = info_df.loc['Lower Bound', 'Value']
        self.upper_bound = info_df.loc['Upper Bound', 'Value']
        self.number_of_quasi_cliques = info_df.loc['Number of Groups', 'Value']


class DataWriter:
    """Writes a partition to a xlsx-file."""

    def __init__(
            self,
            path_to_output_file: Union[str, Path],
            partition: Union[List[List[int]], NDArray[np.int64]]
    ) -> None:
        self.path_to_output_file = path_to_output_file
        data = [[student, group] for group, students
                in enumerate(partition, start=1) for student in students]
        data = sorted(data, key=lambda x: x[0])
        self.students_data = pd.DataFrame(
            data, columns=['Student ID', 'Group']
        )

    def make_file(self) -> None:
        self.students_data.to_excel(
            self.path_to_output_file, sheet_name="students", index=False
        )


class LogParser:
    """Reads a Log-file."""

    LOG_PATTERN = re.compile(
        r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - '
        r'(.+?) - '
        r'(DEBUG|INFO|WARNING|ERROR|CRITICAL) - '
        r'(.+)$'
    )

    def __init__(
            self,
            path_to_log_file: Union[str, Path]
    ) -> None:
        self.path_to_log_file = Path(path_to_log_file)
        self.entries = []
        self.file_name_to_statistics = {
            '2 groups': {},
            'general': {}
        }

    def parse(self) -> None:
        if self.path_to_log_file.exists():
            with open(self.path_to_log_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    match = self.LOG_PATTERN.match(line)
                    if match:
                        entry = {
                            'timestamp': (
                                datetime.strptime(
                                    match.group(1).replace(',', '.'), '%Y-%m-%d %H:%M:%S.%f'
                                )
                            ),
                            'logger': match.group(2).strip(),
                            'level': match.group(3),
                            'message': match.group(4),
                            'raw': line
                        }
                        self.entries.append(entry)

    def make_stistics(self) -> None:
        self.parse()

        for entry in self.entries:
            if (
                entry['logger'] == '__main__'
                and entry['message'].startswith('Start')
                and entry['message'].endswith('.xlsx`.')
            ):
                file_name = (
                    re.search(
                        FILE_NAME_PATTERN,
                        entry['message']
                    ).group()[1:-6]
                )
                if len(file_name) == 7:
                    data_type = '2 groups'
                else:
                    data_type = 'general'

                if file_name not in self.file_name_to_statistics[data_type]:
                    self.file_name_to_statistics[data_type][file_name] = {}

                if 'with symmetries' in entry['message']:
                    model = 'milp_s'
                elif 'without symmetries' in entry['message']:
                    model = 'milp'
                elif 'general' in entry['message']:
                    model = 'general milp'
                else:
                    model = 'greedy algorithm'
                    start_time = entry['timestamp']
                self.file_name_to_statistics[data_type][file_name][model] = {}
            elif entry['message'] == 'Start optimizing.':
                start_time = entry['timestamp']
            elif entry['message'] == 'Finish optimizing.':
                (
                    self.file_name_to_statistics[data_type]
                    [file_name][model]['solving time']
                ) = (entry['timestamp'] - start_time).total_seconds()
            elif 'Minimal density is ' in entry['message']:
                density = re.search(DENSITY_PATTERN, entry['message'])
                if density:
                    (
                        self.file_name_to_statistics[data_type]
                        [file_name][model]['minimal density']
                    ) = float(density.group())
                else:
                    (
                        self.file_name_to_statistics[data_type]
                        [file_name][model]['minimal density']
                     ) = -1
            elif 'Finish greedy' in entry['message']:
                (
                    self.file_name_to_statistics[data_type]
                    [file_name][model]['solving time']
                ) = (entry['timestamp'] - start_time).total_seconds()
            elif 'Solution was not found.' == entry['message']:
                (
                    self.file_name_to_statistics[data_type]
                    [file_name][model]['minimal density']
                 ) = -1

    def make_file(
            self,
            path_to_statistics: Union[str, Path],
    ) -> None:
        self.path_to_statistics = path_to_statistics

        rows_2_groups = []
        rows_general = []

        for file_name in self.file_name_to_statistics['2 groups']:
            row = [
                file_name,
                (
                    self.file_name_to_statistics['2 groups']
                    [file_name]['milp_s']['solving time']
                ),
                (
                    self.file_name_to_statistics['2 groups']
                    [file_name]['milp_s']['minimal density']
                ),
                (
                    self.file_name_to_statistics['2 groups']
                    [file_name]['milp']['solving time']
                ),
                (
                    self.file_name_to_statistics['2 groups'][file_name]
                    ['milp']['minimal density']
                ),
                (
                    self.file_name_to_statistics['2 groups']
                    [file_name]['general milp']['solving time']
                ),
                (
                    self.file_name_to_statistics['2 groups'][file_name]
                    ['general milp']['minimal density']
                ),
                (
                    self.file_name_to_statistics['2 groups'][file_name]
                    ['greedy algorithm']['solving time']
                ),
                (
                    self.file_name_to_statistics['2 groups'][file_name]
                    ['greedy algorithm']['minimal density']
                ),
            ]
            rows_2_groups.append(row)

        for file_name in self.file_name_to_statistics['general']:
            row = [
                file_name,
                (
                    self.file_name_to_statistics['general']
                    [file_name]['milp_s']['solving time']
                ),
                (
                    self.file_name_to_statistics['general']
                    [file_name]['milp_s']['minimal density']
                ),
                (
                    self.file_name_to_statistics['general']
                    [file_name]['milp']['solving time']
                ),
                (
                    self.file_name_to_statistics['general']
                    [file_name]['milp']['minimal density']
                ),
                (
                    self.file_name_to_statistics['general']
                    [file_name]['general milp']['solving time']
                ),
                (
                    self.file_name_to_statistics['general']
                    [file_name]['general milp']['minimal density']
                ),
            ]
            rows_general.append(row)

        general_table = pd.DataFrame(
            rows_general,
            columns=COLUMNS_GENERAL,
        )
        groups_2_table = pd.DataFrame(
            rows_2_groups,
            columns=COLUMNS_2_GROUPS,
        )

        with pd.ExcelWriter(
            self.path_to_statistics,
            engine='openpyxl'
        ) as writer:
            groups_2_table.to_excel(writer, sheet_name='2 groups', index=False)
            general_table.to_excel(writer, sheet_name='general', index=False)


class SolutionReader:
    """Reads solution from xlsx-file."""

    def __init__(
            self,
            path_to_input_file: Union[str, Path],
            path_to_solution_file: Union[str, Path],
    ) -> None:
        students_df = pd.read_excel(
            path_to_solution_file,
            sheet_name='students',
            index_col='Student ID'
        )
        self.data = DataReader(path_to_input_file)
        self.students = students_df.index.tolist()
        data_students = (
            self.data.students_df
            .set_index('Student ID', inplace=False)
        )
        students_df['Previous Group'] = data_students['Group']
        self.sol_partition = (
            students_df
            .groupby('Group')
            .apply(lambda df: df.index.to_list())
            .tolist()
        )
        self.sol_partition_sizes = []
        for _, group1 in students_df.groupby('Group'):
            inner_len = []
            for _, group2 in group1.groupby('Previous Group'):
                inner_len.append(len(group2))
            self.sol_partition_sizes.append(inner_len)
