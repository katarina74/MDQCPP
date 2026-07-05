import re
from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent.parent
INPUT_DIR = BASE_DIR / 'Input'
OUTPUT_DIR = BASE_DIR / 'Output'

EPS = 10e-6

INPUT_2_GROUPS_LEN = 12
INPUT_GENERAL_LEN = INPUT_2_GROUPS_LEN - 2

PATTERN_MILP_G_GENERAL = re.compile(r'milp_g_\d+_\d+_\d+\.xlsx')
PATTERN_MILP_GENERAL = re.compile(r'milp_\d+_\d+_\d+\.xlsx')
PATTERN_MILP_SYM_GENERAL = re.compile(r'milp_s_\d+_\d+_\d+\.xlsx')
PATTERN_MILP_G_2 = re.compile(r'milp_g_\d+_\d+_\d+_\d+\.xlsx')
PATTERN_MILP_2 = re.compile(r'milp_\d+_\d+_\d+_\d+\.xlsx')
PATTERN_MILP_SYM_2 = re.compile(r'milp_s_\d+_\d+_\d+_\d+\.xlsx')
PATTERN_GREEDY = re.compile(r'greedy_\d+_\d+_\d+_\d+\.xlsx')
