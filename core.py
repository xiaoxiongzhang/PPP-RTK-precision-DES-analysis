import os
import time
from typing import Union

import pandas as pd
from config import Content, Config
from common import ReadTable
from algorithm import Algorithm
from plotter import Plotter
from utils import DataFormatHandler
from collections import defaultdict


class Application:
    def __init__(self, content: Union[Content, Config], echo=print):
        self.reader = ReadTable()
        self.CONFIG = content
        self.algorithm = Algorithm(content)
        self.echo = echo

    def handle(self, df_data: pd.DataFrame):
        # 时间格式处理
        f_handler = DataFormatHandler(df_data)
        _format = f_handler.get_format()
        df_data = f_handler.date_convert(_format)

        # self.echo(df_data)
        # 计算收敛时间
        convergence_time, _h_df = self.algorithm.convergence_time_calc(df_data, self.CONFIG.THRESHOLD)
        if _h_df.empty:
            raise Exception("精度计算结束，没有满足连续60条数据连续收敛的数据")
        # 计算精度
        precision = self.CONFIG.PRECISION
        precision_mapping: dict = self.CONFIG.PRECISION_MAPPING
        precision_mapping[-1] = "H"  # 增加H值计算
        ret: defaultdict = defaultdict(float)
        for ind, name in precision_mapping.items():
            ind: int
            name: str
            for p in precision:
                _name = f"{name}_{int(p * 100)}%"
                _ret = self.algorithm.accuracy_calc(_h_df.iloc[:, ind], p)
                ret[_name] = [round(_ret * 100, 2)]

        ret["收敛时间(单位：s)"] = [int(convergence_time)]

        return pd.DataFrame(ret), _h_df

    def single_process(self, path):
        file_name = os.path.basename(path)
        row_df = self.reader.load_data(path, seq=self.CONFIG.SEP)
        _df, _h_df = self.handle(row_df)
        _df: pd.DataFrame
        _df.insert(loc=0, column="文件", value=file_name)
        return _df, _h_df

    def run(self):
        try:
            figure = self.CONFIG.PLOT
            s_time = int(time.time())
            input_path = self.CONFIG.INPUT_PATH
            output_path = self.CONFIG.OUTPUT_PATH
            file_path_list = []

            if not (os.path.exists(input_path) or os.path.isdir(input_path) or os.path.isfile(input_path)):
                self.echo(f"Error!输入路径有误:{input_path}")
                return
            if os.path.isfile(input_path):
                df, fig_df = self.single_process(input_path)
                fig_df_list = [fig_df]
                file_path_list = [os.path.join(output_path, os.path.basename(input_path))]
            else:
                df_list = []
                fig_df_list = []
                file_list = os.listdir(input_path)
                for f in file_list:
                    f_path = os.path.join(input_path, f)
                    _df, _h_df = self.single_process(f_path)
                    df_list.append(_df)
                    fig_df_list.append(_h_df)
                    file_path_list.append(os.path.join(output_path, f))

                df = pd.concat(df_list, axis=0, ignore_index=True)

            if df.empty:
                assert Exception("Error：结果数据为空！")
            df.set_axis([f"{i + 1}" for i in range(len(df))], axis=0, inplace=True)
            print(df)
            df.to_csv(os.path.join(self.CONFIG.OUTPUT_PATH, "result.csv"), sep="\t")
            df.to_excel(os.path.join(self.CONFIG.OUTPUT_PATH, "result.xlsx"))
            # 绘图
            if figure:
                plot = Plotter(self.CONFIG)
                for _i, _df in enumerate(fig_df_list):
                    fig = plot.plot(_df, self.CONFIG.SHOW_PIC)
                    Plotter.save(fig, file_path_list[_i] + ".png")
        except Exception as e:
            self.echo(e)
            self.echo("程序异常，请检查输入文件数据结构格式是否正确，如确认数据无误请联系开发人员！")

        else:
            self.echo(f"数据统计分析成功！用时：{int(time.time() - s_time)} 秒")
            self.echo(f"数据处理完成，请到【{self.CONFIG.OUTPUT_PATH}】路径下查看结果文件！")


if __name__ == '__main__':
    from config import Content, CONFIG

    c = Content(
        INPUT_PATH=CONFIG.INPUT_PATH,
        COLUMNS=CONFIG.COLUMNS,
        THRESHOLD=CONFIG.THRESHOLD,
        PRECISION=CONFIG.PRECISION,
        PRECISION_MAPPING=CONFIG.PRECISION_MAPPING,
        OUTPUT_PATH=CONFIG.OUTPUT_PATH,
        PLOT=CONFIG.PLOT,
        SHOW_PIC=CONFIG.SHOW_PIC,
        TRUNCATE=CONFIG.TRUNCATE,
        SEP=CONFIG.SEP,
    )

    Application(c).run()
