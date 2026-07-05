import logging
import os
from os.path import isfile, join
from pathlib import Path

from src.constants import (
    INPUT_DIR,
    LOG_FILE_NAME,
    OUTPUT_DIR,
    STATISTICS_FILE_NAME,
    TIMELIMIT
)
from src.data_processing import DataReader, DataWriter, LogParser
from src.greedy_algorithm import get_partition_sizes_by_sizes_of_cliques
from src.milp import run_milp_cliques_model
from src.milp_general import run_milp_general_model
from src.utils import (
    get_edges_by_partition,
    get_min_density_by_sizes,
    get_partition_by_sizes
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_NAME, mode='w'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

files = [
     Path(join(INPUT_DIR, f)) for f in
     os.listdir(INPUT_DIR) if isfile(join(INPUT_DIR, f))
]
Path(OUTPUT_DIR).mkdir(exist_ok=True)

for file_name in files:
    data_reader = DataReader(file_name)

    logger.info('Start optimizing milp model with symmetries '
                f'breaking constraints for file `{file_name.name}`.')

    gamma_value_milp_s, partition_milp_s = run_milp_cliques_model(
        data_reader.students,
        data_reader.number_of_quasi_cliques,
        data_reader.lower_bound,
        data_reader.upper_bound,
        data_reader.old_partition_num,
        data_reader.old_partition,
        timelimit=TIMELIMIT,
        break_symmetries_q=True
    )
    if partition_milp_s is not None:
        DataWriter(
             join(OUTPUT_DIR, 'milp_s_' + file_name.name),
             partition_milp_s
        ).make_file()

    logger.info('Finish optimizing milp model with symmetries '
                f'breaking constraints for file `{file_name.name}`.')

    logger.info('Start optimizing milp model without symmetries '
                f'breaking constraints for file `{file_name.name}`.')

    gamma_value_milp, partition_milp = run_milp_cliques_model(
        data_reader.students,
        data_reader.number_of_quasi_cliques,
        data_reader.lower_bound,
        data_reader.upper_bound,
        data_reader.old_partition_num,
        data_reader.old_partition,
        timelimit=TIMELIMIT,
        break_symmetries_q=False
    )

    if partition_milp is not None:
        DataWriter(
            join(OUTPUT_DIR, 'milp_' + file_name.name),
            partition_milp
        ).make_file()

    logger.info('Finish optimizing milp model without symmetries '
                f'breaking constraints for file `{file_name.name}`.')

    logger.info('Start optimizing general milp model for '
                f'for file `{file_name.name}`.')

    gamma_value_milp_g, partition_milp_g = run_milp_general_model(
        data_reader.students,
        data_reader.number_of_quasi_cliques,
        data_reader.lower_bound,
        data_reader.upper_bound,
        get_edges_by_partition(data_reader.old_partition),
        timelimit=TIMELIMIT,
    )

    if partition_milp_g is not None:
        DataWriter(
            join(OUTPUT_DIR, 'milp_g_' + file_name.name),
            partition_milp_g
        ).make_file()

    logger.info(
        f'Finish optimizing general milp model for file `{file_name.name}`.'
    )

    if len(file_name.name) == 12:
        logger.info('Start greedy algorithm '
                    f'for file `{file_name.name}`.')

        partition_sizes = get_partition_sizes_by_sizes_of_cliques(
                data_reader.old_partition_num
        )
        partition_greedy = get_partition_by_sizes(
            partition_sizes,
            data_reader.old_partition
        )
        gamma_value_greedy = get_min_density_by_sizes(partition_sizes)
        logger.info(f"Minimal density is {gamma_value_greedy}.")

        if partition_greedy is not None:
            DataWriter(
                join(OUTPUT_DIR, 'greedy_' + file_name.name),
                partition_greedy
            ).make_file()

        logger.info(f'Finish greedy algorithm for file `{file_name.name}`.')

log_parser = LogParser(LOG_FILE_NAME)
log_parser.make_stistics()
log_parser.make_file(STATISTICS_FILE_NAME)
