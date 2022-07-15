import pandas as pd
import math

from common import LoadConfig


class Algorithm(LoadConfig):
    def convergence_time_calc(self, data: pd.DataFrame, threshold: float):
        """收敛时间算法。
        :param threshold: 阈值，收敛时间计算条件, 单位cm。
        :param data: 传入数据。
        :return: （Int 秒, 计算H之后的df）
        """
        if data.empty or len(data) < 60:
            return
        e_index = self.CONFIG.COLUMNS[0]
        n_index = self.CONFIG.COLUMNS[1]
        u_index = self.CONFIG.COLUMNS[2]
        threshold = threshold / 100  # cm -> m

        data_c = data.copy()
        # 剔除结果必为 0 的数据
        data_c = data_c[
            (data_c.iloc[:, e_index] != 0) & (data_c.iloc[:, u_index] != 0) & (data_c.iloc[:, n_index] != 0)]
        data_c["H"] = (data_c.iloc[:, e_index].astype(float) ** 2 + data_c.iloc[:, n_index].astype(float) ** 2).apply(
            func=math.sqrt)
        data_len = len(data_c)
        _iter = iter(range(data_len))
        ind = None
        for _ind in _iter:
            if data_len - _ind <= 60:
                print("convergence_time_calc：剩余数据少于验证数据数量：60")
                data_c = pd.DataFrame()
                break
            if data_c["H"].iloc[_ind] <= threshold:
                df_60: pd.DataFrame = data_c.iloc[_ind + 1:_ind + 61]
                if len(df_60[df_60["H"] <= threshold]) == 60:
                    ind = _ind
                    if self.CONFIG.TRUNCATE:
                        data_c = data_c.iloc[_ind:]  # 截取满足条件的数据 进行后续的画图和精度计算
                    break
                target_ind = df_60[df_60["H"] > threshold].iloc[-1].name
                for _ in range(target_ind - _ind):
                    next(_iter)

        if ind is None:
            return 0, pd.DataFrame()
        start_time = data.at[0, "datetime"]
        end_time = data_c.at[ind, "datetime"]
        convergence_time = end_time - start_time
        return convergence_time, data_c

    @staticmethod
    def accuracy_calc(data: pd.Series, precision: float):
        """精度计算。
        :param data: 传入数据
        :param precision: 精度
        """
        if data.empty:
            return
        if precision <= 0:
            raise Exception("accuracy_calc： precision值必须在0~1内")
        data = data.apply(func=abs)
        sorted_data = data.sort_values()
        per_result = sorted_data.iloc[int(len(data) * precision)]
        return per_result


if __name__ == '__main__':
    from config import CONFIG

    s = pd.Series([i for i in range(10)])
    ret = Algorithm(CONFIG).accuracy_calc(s, 0.5)
    print(ret)
