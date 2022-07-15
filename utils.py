import configparser
import time
from enum import Enum

import pandas as pd


def read_ini(path):
    """读取ini配置文件方法"""
    conf = configparser.RawConfigParser()
    conf.read(path, encoding="utf-8")
    return conf


class FormatTypeEnum(Enum):
    POS = "pos"
    TXT = "txt"


class DataFormatHandler:
    """判断输入文件的内容格式类型
    目前有2种类型：
        txt: 年、月、日、时、分、秒、east_float、north_float 、up_float、east_fixed、north_fixed、up_fixed、卫星数、参与固定模糊度数、固定成功模糊度数、FFratio 值、阈值、GPS系统基准星、Galileo系统基准星、BDS系统基准星、x_float、y_float、z_float、x_fixed、y_fixed、z_fixed
        pos: 定位状态、年月日、时分秒、east_float、north_float 、up_float、east_fixed、north_fixed、up_fixed、卫星数、参与固定模糊度数、固定成功模糊度数、FFratio 值、阈值、GPS系统基准星、Galileo系统基准星、BDS系统基准星、x_float、y_float、z_float、x_fixed、y_fixed、z_fixed
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_format(self):
        el: str = str(self.df[0].iat[0]).upper()
        if el.startswith("POS"):
            return FormatTypeEnum.POS
        else:
            return FormatTypeEnum.TXT

    def date_convert(self, format_type: FormatTypeEnum):
        """输入数据时间格式处理"""
        try:
            df = self.df.copy()
            if format_type == FormatTypeEnum.POS:
                df["datetime"] = df[1] + " " + df[2].apply(
                    func=lambda s: s.split(".")[0]
                )
            elif format_type == FormatTypeEnum.TXT:
                df["datetime"] = df[0].astype(str) + "/" + df[1].astype(str) + "/" + df[2].astype(
                    str) + " " + df[3].astype(str) + ":" + df[4].astype(str) + ":" + df[5].astype(int).astype(str)

            df["datetime"] = df["datetime"].apply(
                func=lambda d: int(time.mktime(time.strptime(d, "%Y/%m/%d %H:%M:%S"))))
        except Exception as e:
            print(e)
            print(df.head(3))
            raise Exception("输入数据时间格式有误")
        return df


def echo_log(content: str):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    return f"[{time_str}]  {content}"


if __name__ == '__main__':
    c = read_ini("./config.ini")
    print(c)
    print(c.items("source"))
    print(dict(c.items("source")))
