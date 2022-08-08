## ppp-rtk精度统计测试工具

---
### 工具介绍：
因为数据中的时间格式问题，目前仅支持时间格式为提供的2种：
- 2022/06/20 07:41:39.000
- 2022 06 20 07 42 57.000 

---
### 使用介绍：

#### 工具准备：
- Python3.6+ （推荐同开发环境版本一致：Python3.9）

#### 使用说明：

> **支持2种使用方式：**
>
> 		1. 终端直接调用源代码
> 		1. GUI图形化界面

---

##### 1.  终端调用

- 确认电脑上已经安装了Python3.9环境，并添加到环境变量

- 在本项目目录下打开终端
  - windows下操作： 打开本项目路径（跟main.py同级目录）
  - 在文件资源管理器的路径栏上输入：cmd
  
- 相关依赖下载，在终端中输入：
  ``` text
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
  
- 打开目录下 config.ini 配置文件，根据需要调整相关输入配置：
  ``` ini 
  [source]
  # 输入数据文件路径，文件或者文件夹
  path=C:/Users/ThinkBook/PycharmProjects/GYSS_IGG/data/dir
  ;path=C:/Users/ThinkBook/PycharmProjects/GYSS_IGG/data/GYSS_IGG.pos
  
  # 文件类数据列分隔符，空格分隔符不填即可
  sep=
  
  # E N U 数据列号（从0开始计数， 顺序为 E,N,U） 用来计算H值
  columns=[6, 7, 8]
  
  # 收敛时间计算阈值，单位cm
  threshold=30
  
  # 精度需求
  precision=[0.68, 0.95]
  
  # 需要展示精度分析的列名和列索引
  # 列索引： 从0开始技术， 按分隔符进行分隔。如：
  # 数   据:  1  2  3  4.1  5  6  7  0.11
  # 对应索引:  0  1  2   3   4  5  6   7
  # eg:
  #   {该列在源数据中的位置（索引）: 需要展示的列名称， ...}
  precision_mapping = {6: "E", 7: "N", 8: "U"}
  
  [output]
  # 输出文件路径
  path=C:/Users/ThinkBook/PycharmProjects/GYSS_IGG/output1/
  
  # 是否输出分析图片: True / False
  plot=False
  
  # 是否展示分析图片: True / False
  show_pic=False
  
  # 是否剔除未收敛的数据: True / False
  truncate=False
  
  ```

- 在代码根目录（即main.py同级目录下）的终端中运行：

  ```
  python main.py
  ```

- 等待程序运行完成，输出文档在config.ini 中配置的output输出路径下。


---

##### 2. 图形化GUI使用

- **方式 1**：图形化GUI 程序源代码直接使用：

  - 在代码根目录（即main.py同级目录下）的终端中运行：

    ~~~ 
    python gui.py 
    ~~~

- **方式 2**：图形化GUI程序打包使用：

  - exe软件打包：

    - 在代码根目录（即main.py同级目录下）的终端中运行：

      ~~~ 
      pyinstaller -F -w -i ./icon.ico gui.py -p ./dist
      ~~~

  - 生成的.exe文件在 ./dist 目录下，直接双击使用即可。

---

