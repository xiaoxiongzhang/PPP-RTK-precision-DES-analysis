import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from core import Application
from typing import Literal

from config import Content
from tool_gui import Ui_MainWindow as UiMainWindow
from utils import echo_log

# 分隔符映射
sep_map = {
    "(空格)": " ",
    ",": ",",
    "/": "/",
    ".": ".",
    "|": "|"
}


class ToolGui(QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(ToolGui, self).__init__(parent)
        self.setupUi(self)

        self.comboBox_sep.addItems(sep_map.keys())
        self.button_start.clicked.connect(self.handle)
        self.plainTextEdit_echo.setMaximumBlockCount(500)
        self.echo = lambda s: self.plainTextEdit_echo.appendPlainText(echo_log(s))
        self.radioButton_gen_pic.clicked.connect(self.pic_show_switch)
        self.toolButton_file.clicked.connect(self.set_path("source"))
        self.toolButton_file_2.clicked.connect(self.set_path("target"))

    def set_path(self, which: Literal["source", "target"]):

        def set_source():
            path = QFileDialog.getExistingDirectory(self, "选择源数据文件路径", "./")
            self.lineEdit_source.setText(path)

        def set_target():
            path = QFileDialog.getExistingDirectory(self, "选择输出文件路径", "./")
            self.lineEdit_target.setText(path)

        _d = {
            "source": set_source,
            "target": set_target,
        }
        return _d.get(which)

    def pic_show_switch(self):
        """分析图片radio选择框 是否可用 开关"""
        if self.radioButton_gen_pic.isChecked():
            self.radioButton_show_pic.setEnabled(True)
            self.label_show_pic.setEnabled(True)

        else:
            self.radioButton_show_pic.setEnabled(False)
            self.label_show_pic.setEnabled(False)
            self.radioButton_show_pic.setChecked(False)

    def get_content(self):
        """窗体内容获取"""
        e_value = self.spinBox_e.value()
        n_value = self.spinBox_n.value()
        u_value = self.spinBox_u.value()

        try:
            threshold = int(self.lineEdit_threshold.text())
        except:
            QMessageBox.information(self, "Error", "【收敛阈值】输入格式错误，请确认输入格式，示例：30 ")
            return

        try:
            precision = self.lineEdit_precision.text().replace("；", ";")
            precision = list(map(lambda _p: float(_p), precision.split(";")))
        except:
            QMessageBox.information(self, "Error", "【精度需求】输入格式错误，请确认输入格式，示例：0.68; 0.95 ")
            return

        try:
            precision_mapping = self.plainTextEdit_col_map.toPlainText().replace("，", ",")
            precision_mapping = precision_mapping.replace("\r\n", ";#").replace("\n", ";#").replace("\r", ";#")
            _p_list = list(
                map(
                    lambda s: s.split(","),
                    filter(
                        lambda i: str(i),
                        map(
                            lambda el: el.replace(" ", ""), precision_mapping.split(";#")
                        )
                    )
                )
            )
            for _p in _p_list:
                _p[0] = int(_p[0])
            precision_dict = dict(_p_list)
        except:
            QMessageBox.information(self, "Error", "【精度分析列数据位置映射】输入格式错误，请确认输入格式，示例：6, H值")
            return

        content = Content(
            INPUT_PATH=self.lineEdit_source.text().strip(),  # 源路径
            COLUMNS=[e_value, n_value, u_value],  # E，N，U
            THRESHOLD=threshold,  # 收敛阈值
            PRECISION=precision,  # 精度
            PRECISION_MAPPING=precision_dict,  # 精度列数据
            OUTPUT_PATH=self.lineEdit_target.text().strip(),  # 输出路径
            PLOT=self.radioButton_gen_pic.isChecked(),  # 是否生成图片
            SHOW_PIC=self.radioButton_show_pic.isChecked(),  # 是否展示图片
            TRUNCATE=self.radioButton_truncate.isChecked(),  # 是否剔除未收敛数据
            SEP=sep_map[self.comboBox_sep.currentText()],  # 分隔符
        )

        return content

    def handle(self):
        """分析按钮slot"""
        self.button_start.setText("处理中...")
        self.button_start.setEnabled(False)
        config = self.get_content()
        print(config)

        try:
            if config:
                _app = Application(config, self.echo)
                _app.run()
                self.echo("分析完成！")
        except:
            QMessageBox.information(self, "Error", "程序异常，请检查输入文件数据结构格式是否正确，如确认数据无误请联系开发人员！")
        finally:
            self.button_start.setText("开始分析")
            self.button_start.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_w = ToolGui()

    main_w.show()
    sys.exit(app.exec_())
