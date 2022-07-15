import json
import os
import platform
from typing import Optional

from utils import read_ini
import ast
from dataclasses import dataclass, field

PLATFORM = platform.system()

BASE_PATH = os.getcwd()
CONFIG_PATH = os.path.join(BASE_PATH, "config.ini")


@dataclass
class Content:
    INPUT_PATH: str
    COLUMNS: list
    THRESHOLD: float
    PRECISION: list
    PRECISION_MAPPING: dict
    OUTPUT_PATH: str
    PLOT: bool
    SHOW_PIC: bool
    TRUNCATE: bool
    SEP: Optional[str] = field(default=" ")


def read_config(section):
    ret = {}
    try:
        conf = read_ini(CONFIG_PATH)
        ret = dict(conf.items(section))
    except Exception as e:
        print(e)
        print(f"{CONFIG_PATH} 配置中没有 {section} section")
    return ret


class Config:
    BASE_PATH = BASE_PATH
    CONFIG_PATH = CONFIG_PATH
    SOURCE = read_config("source")
    OUTPUT = read_config("output")

    INPUT_PATH = SOURCE.get("path", "")
    SEP = SOURCE.get("sep") or " "
    COLUMNS = json.loads(SOURCE.get("columns", "[]"))
    THRESHOLD = float(SOURCE.get("threshold", 0))
    PRECISION = json.loads(SOURCE.get("precision", "[]"))
    PRECISION_MAPPING = ast.literal_eval(SOURCE.get("precision_mapping", "{}"))
    OUTPUT_PATH = OUTPUT.get("path", "")
    PLOT = ast.literal_eval(OUTPUT.get("plot", "False"))
    SHOW_PIC = ast.literal_eval(OUTPUT.get("show_pic", "False"))
    TRUNCATE = ast.literal_eval(OUTPUT.get("truncate", "False"))

    def __init__(self):
        if self.INPUT_PATH and not os.path.exists(self.INPUT_PATH):
            os.mkdir(self.INPUT_PATH)
        if self.OUTPUT_PATH and not os.path.exists(self.OUTPUT_PATH):
            os.mkdir(self.OUTPUT_PATH)


CONFIG = Config()

if __name__ == '__main__':
    print(os.getcwd())
    print(os.path.join("ss", "qq"))
    """
C:/Users/ThinkBook/PycharmProjects/GYSS_IGG/data/dir/GYSS_DPI_PPP.txt
C:/Users/ThinkBook/PycharmProjects/GYSS_IGG/output/

0.68；0.95
    
6，e
7,n
8,u
    """
