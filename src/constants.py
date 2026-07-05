from pathlib import Path

BIG_M = 10_000
TIMELIMIT = 3600

FILE_NAME_PATTERN = r'`(\d+(?:_\d+)*)\.xlsx`'
DENSITY_PATTERN = r'\d+\.\d+'

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / 'Input'
OUTPUT_DIR = BASE_DIR / 'Output'
LOG_FILE_NAME = BASE_DIR / 'log.log'
STATISTICS_FILE_NAME = OUTPUT_DIR / 'statistics.xlsx'

INDEX_COL = 'instance'
MILP_S_SOLVING_TIME_COL = 'milp + symmetries-breaking solving time'
MILP_S_DENSITY_COL = 'milp + symmetries-breaking minimal density'
MILP_SOLVING_TIME_COL = 'milp solving time'
MILP_DENSITY_COL = 'milp minimal density'
MILP_G_SOLVING_TIME_COL = 'general milp solving time'
MILP_G_DENSITY_COL = 'general milp minimal density'
GREEDY_SOLVING_TIME_COL = 'greedy algorithm solving time'
GREEDY_DENSITY_COL = 'greedy algorithm minimal density'

COLUMNS_GENERAL = [
    INDEX_COL,
    MILP_S_SOLVING_TIME_COL,
    MILP_S_DENSITY_COL,
    MILP_SOLVING_TIME_COL,
    MILP_DENSITY_COL,
    MILP_G_SOLVING_TIME_COL,
    MILP_G_DENSITY_COL,
]
COLUMNS_2_GROUPS = COLUMNS_GENERAL + [
    GREEDY_SOLVING_TIME_COL,
    GREEDY_DENSITY_COL,
]
