import os.path
from typing import Union
import matplotlib.pyplot as plt
import time
import pandas as pd

from config import Content, Config


class Plotter:

    def __init__(self, content: Union[Content, Config]):
        self.CONFIG = content
        self.precision_mapping: dict = content.PRECISION_MAPPING  # py3.6之后dict有序

    def plot(self, data: Union[pd.DataFrame, pd.Series], show: bool = False):

        if isinstance(data, pd.Series):
            fig = data.plot()
        else:
            data_len = len(data)
            step = int(data_len / 8)
            time_data = data["datetime"].astype(int).apply(
                lambda t: time.strftime("%H:%M", time.localtime(t))
            ).to_list()[::step]
            fig = plt.figure()
            # plt.subplots_adjust(hspace=0.3)
            plt.xticks([i for i in range(len(time_data))], time_data)
            plt.yticks([i for i in range(len(time_data))], ["" for i in range(len(time_data))])
            _n = len(self.precision_mapping)
            for _ind, c in enumerate(self.precision_mapping.keys()):
                name = self.precision_mapping[c]
                _ax = fig.add_subplot(_n, 1, _ind + 1)
                _ax.plot(data.iloc[:, c] * 100, ",")
                _ax.grid(linewidth=0.2)
                _ax.xaxis.set_ticks([i for i in range(len(time_data))], ["" for i in range(len(time_data))])
                # _ax.legend(title=f"name")  # TODO
                _ax.set_ylabel(name)

        if show:
            plt.show()
        return fig

    @staticmethod
    def save(fig, file_path):
        fig.suptitle(os.path.basename(file_path).rsplit(".", 1)[0])
        fig.savefig(file_path)
