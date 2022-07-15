import abc

import pandas as pd
from typing import List, Optional, Union

# pd.set_option("display.unicode.ambiguous_as_wide", True)
# pd.set_option("display.unicode.east_asian_width", True)
from config import Content, Config


class LoadConfig:
    def __init__(self, content: Union[Content, Config]):
        self.CONFIG = content


class ReadData(metaclass=abc.ABCMeta):
    """读取文件数据抽象类"""

    @abc.abstractmethod
    def load_data(self, path: str, **kwargs):
        ...


class ReadTable(ReadData):
    """读取二维行列非表格文件数据"""

    def load_data(self, path: str, seq: str = " ", loc: List[int] = None) -> Optional[pd.DataFrame]:
        """从指定路径文件读取数据。
        :param path: 数据文件路径
        :param seq: 数据分隔符
        :param loc: 需要读取的列
        """
        header = None
        if seq.isspace():
            data = pd.read_table(path, delim_whitespace=True, header=header)
        else:
            data = pd.read_table(path, sep=seq, header=header)
        if data.empty:
            return
        if loc:
            data = data.iloc[:, loc]
        return data


if __name__ == '__main__':
    from utils import DataFormatHandler, FormatTypeEnum
    import matplotlib.pyplot as plt

    _path = r".\data\GYSS_IGG.pos"
    # _path = r".\data"
    r = ReadTable()
    d = r.load_data(_path)
    # d = d.tail(5)
    # d["h"] = d[1] ** 2 + d[2] ** 2
    d["H"] = d[25]
    print(d)
    print(d.at[60141, "H"])
    # print(d[d[0] > 3])
    # print(d.iloc[1:, 1])

    # fig = plt.figure()
    # fig.suptitle("ssdf")
    #
    #
    # # for i in [1, 2]:
    # #     ax = fig.add_subplot(2, 1, i)
    # #     ax.plot(d[7 if i == 1 else 6])
    #
    # ax1 = fig.add_subplot(2, 1, 1)
    # ax2 = fig.add_subplot(2, 1, 2)
    # ax2.plot(d[7], ".", markersize=0.1)
    # ax1.plot(d[6], ",", markersize=5)

    # ax1.set_ylabel("123")
    # ax1.legend(title='hello')
    # ax1.grid(linewidth=0.2)

    #
    # a = d[7].plot()
    # f = d[8].plot()

    # plt.show()
    # fig.savefig("./xxx.png")

    # d.to_csv("./ret.csv", sep="\t", index=False, header=["id", "文件", "水平68%", "高程68%", "水平95%", "高程95%", "收敛时间"])
    # print(abs(d[0]))
