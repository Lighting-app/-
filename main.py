from PyQt5.Qt import *
import pyqtgraph as pg
import serial
import serial.tools.list_ports
import images


class MenuAction(QAction):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.triggered.connect(lambda: self.click_event())
        self.is_clicked = 0

    def click_event(self):
        self.is_clicked = 1

    def click_event_clear(self):
        self.is_clicked = 0


class Window(QWidget):
    """ Window() """

    # 初始化
    def __init__(self):
        super().__init__()  # 初始化父类
        # 建立ui
        # 主窗口(图像窗口、功能面板)
        layout_win = QVBoxLayout(self)  # 创建0级垂直布局管理器layout_win
        layout_win.setContentsMargins(0, 0, 0, 0)  # 设置布局管理器与窗口四个边沿的距离0
        self.setWindowTitle("串口示波器-作者：龙龙(投食QQ:1161057545)")  # 设置窗口标题
        self.resize(500, 500)  # 设置窗口大小
        self.setLayout(layout_win)  # 设置窗口的布局为0级布局管理器layout_win

        # 图像窗口
        self.graph_win = pg.GraphicsLayoutWidget(self)  # 创建图像窗口控件graph_win
        self.graph0 = self.graph_win.addPlot()  # 创建图像graph0
        self.curve0 = self.graph0.plot(pen="r")  # 创建曲线curve0
        self.curve1 = self.graph0.plot(pen="g")
        self.curve2 = self.graph0.plot(pen="b")
        self.curve3 = self.graph0.plot(pen="w")
        self.curve4 = self.graph0.plot(pen="r")  # 创建曲线curve0
        self.curve5 = self.graph0.plot(pen="g")
        self.curve6 = self.graph0.plot(pen="b")
        self.curve7 = self.graph0.plot(pen="w")
        layout_func = QHBoxLayout()  # 创建1级水平布局管理器layout_func
        layout_func.setContentsMargins(0, 0, 10, 0)
        layout_win.addWidget(self.graph_win)  # 将图像窗口控件graph_win添加到0级布局管理器layout_win
        layout_win.addLayout(layout_func)  # 将1级布局管理器layout_func添加到0级布局管理器layout_win

        # 功能面板(标签面板、键盘、文本编辑器)
        # 标签面板
        layout_label = QVBoxLayout(self)
        label1 = QLabel(self)
        label1.setText("串    口:")
        layout_label.addWidget(label1)
        label2 = QLabel(self)
        label2.setText("波 特 率:")
        layout_label.addWidget(label2)
        label6 = QLabel(self)
        label6.setText("通道数量:")
        layout_label.addWidget(label6)
        label3 = QLabel(self)
        label3.setText("串口开关:")
        layout_label.addWidget(label3)

        layout_label.setContentsMargins(10, 0, 0, 0)
        layout_func.addLayout(layout_label)

        # 键盘
        layout_key = QVBoxLayout(self)  # 创建2级垂直布局管理器layout2
        # 串口列表按键
        self.key_com = QPushButton(self)  # 创建按钮key0
        self.menu_com = QMenu(self.key_com)  # 创建com按键菜单
        self.key_com.setMenu(self.menu_com)  # 添加按钮菜单到按键
        layout_key.addWidget(self.key_com)  # 将按钮key0添加到2级布局管理器layout2
        # 波特率选择键
        self.key_baud = QPushButton(self)
        self.menu_baud = QMenu(self.key_baud)
        action_baud1 = QAction("1200", self.menu_baud)
        action_baud2 = QAction("9600", self.menu_baud)
        action_baud3 = QAction("38400", self.menu_baud)
        action_baud4 = QAction("115200", self.menu_baud)
        self.menu_baud.addAction(action_baud1)
        self.menu_baud.addAction(action_baud2)
        self.menu_baud.addAction(action_baud3)
        self.menu_baud.addAction(action_baud4)
        action_baud1.triggered.connect(lambda: self.com_set_baudrate(1200))
        action_baud2.triggered.connect(lambda: self.com_set_baudrate(9600))
        action_baud3.triggered.connect(lambda: self.com_set_baudrate(38400))
        action_baud4.triggered.connect(lambda: self.com_set_baudrate(115200))
        self.key_baud.setMenu(self.menu_baud)
        layout_key.addWidget(self.key_baud)
        # 通道数量按键
        self.key_ch = QPushButton(self)
        menu_ch = QMenu(self.key_ch)
        action_ch1 = QAction("1", menu_ch)
        action_ch2 = QAction("2", menu_ch)
        action_ch4 = QAction("4", menu_ch)
        action_ch8 = QAction("8", menu_ch)
        action_ch1.triggered.connect(lambda: self.graph_set_ch_num(1))
        action_ch2.triggered.connect(lambda: self.graph_set_ch_num(2))
        action_ch4.triggered.connect(lambda: self.graph_set_ch_num(4))
        action_ch8.triggered.connect(lambda: self.graph_set_ch_num(8))
        menu_ch.addAction(action_ch1)
        menu_ch.addAction(action_ch2)
        menu_ch.addAction(action_ch4)
        menu_ch.addAction(action_ch8)
        self.key_ch.setMenu(menu_ch)
        layout_key.addWidget(self.key_ch)
        # 开关串口按键
        self.key_com_switch = QPushButton(QIcon(":/images/close_icon.png"), "", self)
        self.key_com_switch.clicked.connect(lambda: self.com_open())
        layout_key.addWidget(self.key_com_switch)

        layout_func.addLayout(layout_key)  # 加入键盘

        layout_label_right = QVBoxLayout(self)
        label_r2 = QLabel(self)
        label_r2.setText(" 缓存大小:")
        layout_label_right.addWidget(label_r2)
        label_r2 = QLabel(self)
        label_r2.setText(" 图像显示:")
        layout_label_right.addWidget(label_r2)
        label_r2 = QLabel(self)
        label_r2.setText(" 文本显示:")
        layout_label_right.addWidget(label_r2)
        label_r2 = QLabel(self)
        label_r2.setText(" 清空显示:")
        layout_label_right.addWidget(label_r2)
        layout_func.addLayout(layout_label_right)

        layout_key_right = QVBoxLayout(self)
        # 图像缓存大小设置按键
        self.key_graph_len = QPushButton(self)
        menu_graph_len = QMenu(self.key_graph_len)
        action_graph_len0 = QAction("100", menu_graph_len)  # 创建动作
        action_graph_len1 = QAction("200", menu_graph_len)
        action_graph_len2 = QAction("500", menu_graph_len)
        action_graph_len3 = QAction("1000", menu_graph_len)
        action_graph_len0.triggered.connect(lambda: self.graph_set_len_x(100))  # 连接动作触发信号
        action_graph_len1.triggered.connect(lambda: self.graph_set_len_x(200))
        action_graph_len2.triggered.connect(lambda: self.graph_set_len_x(500))
        action_graph_len3.triggered.connect(lambda: self.graph_set_len_x(1000))
        menu_graph_len.addAction(action_graph_len0)  # 添加动作到菜单
        menu_graph_len.addAction(action_graph_len1)
        menu_graph_len.addAction(action_graph_len2)
        menu_graph_len.addAction(action_graph_len3)
        self.key_graph_len.setMenu(menu_graph_len)
        layout_key_right.addWidget(self.key_graph_len)
        # 开关图像显示按键
        self.key_graph_switch = QPushButton(self)
        self.key_graph_switch.clicked.connect(lambda: self.graph_on())
        layout_key_right.addWidget(self.key_graph_switch)
        # 开关文本显示按键
        self.key_text_switch = QPushButton(self)
        self.key_text_switch.clicked.connect(lambda: self.text_on())
        layout_key_right.addWidget(self.key_text_switch)
        # 文本清除按键
        key_text_clean = QPushButton(QIcon(":/images/clean_icon.png"), "", self)
        key_text_clean.clicked.connect(lambda: self.clear_all())
        layout_key_right.addWidget(key_text_clean)

        layout_func.addLayout(layout_key_right)

        # 文本编辑器
        self.editor = QTextEdit(self)  # 创建文本编辑器editor
        self.editor.setReadOnly(True)  # 设置文本编辑器为只读模式
        self.editor.setMaximumHeight(130)  # 设置文本编辑器最大高度150像素
        # self.editor.setMinimumHeight(130)
        layout_func.addWidget(self.editor)  # 将文本编辑器editor添加到一级布局管理器layout_func

        # 初始配置
        self.com_now = None  # 当前串口
        self.com_opt_obj = None  # 串口操作对象，打开串口后创建
        self.com_baudrate = 0   # 串口波特率
        self.com_action_list = []  # 串口菜单列表
        self.com_list = []  # 串口列表
        self.max_len_x = 100  # x轴最大长度
        self.text_en = True  # 文本显示使能
        self.graph_en = True
        self.com_buf = None
        self.graph_y = []
        self.ch_num = 8
        self.graph_ch1_y = []
        self.graph_ch2_y = []
        self.graph_ch3_y = []
        self.graph_ch4_y = []
        self.graph_ch5_y = []
        self.graph_ch6_y = []
        self.graph_ch7_y = []
        self.graph_ch8_y = []

        self.com_refresh()  # 刷新串口
        self.text_off()  # 打开文本显示
        self.com_set_baudrate(115200)  # 设置默认串口波特率
        self.graph_set_ch_num(1)
        self.graph_set_len_x(100)
        self.graph_on()

        timer_refresh = QTimer(self)  # 数据刷新定时器
        timer_refresh.timeout.connect(lambda: self.refresh())  # 连接数据刷新函数
        timer_refresh.start(100)  # 刷新周期设置

    def graph_on(self):
        self.graph_en = True
        self.key_graph_switch.setIcon(QIcon(":/images/graph_on_icon.png"))
        self.key_graph_switch.disconnect()
        self.key_graph_switch.clicked.connect(lambda: self.graph_off())

    def graph_off(self):
        self.graph_en = False
        self.key_graph_switch.setIcon(QIcon(":/images/graph_off_icon.png"))
        self.key_graph_switch.disconnect()
        self.key_graph_switch.clicked.connect(lambda: self.graph_on())

    def graph_set_len_x(self, len_x):
        self.max_len_x = len_x
        self.key_graph_len.setText(str(self.max_len_x))

    # 输出图像
    def graph_output(self, vector_x, vector_y):
        self.curve0.setData(vector_x, vector_y)

    def graph_clear(self):
        self.curve0.setData([], [])
        self.curve1.setData([], [])
        self.curve2.setData([], [])
        self.curve3.setData([], [])
        self.curve4.setData([], [])
        self.curve5.setData([], [])
        self.curve6.setData([], [])
        self.curve7.setData([], [])
        self.graph_ch1_y.clear()
        self.graph_ch2_y.clear()
        self.graph_ch3_y.clear()
        self.graph_ch4_y.clear()
        self.graph_ch5_y.clear()
        self.graph_ch6_y.clear()
        self.graph_ch7_y.clear()
        self.graph_ch8_y.clear()
        self.graph_y.clear()

    # 输出文本
    def text_refresh(self):
        if self.text_en is False:
            return
        try:
            self.editor.insertPlainText(self.com_buf.decode("gbk"))
        except Exception as e:
            self.text_off()
            print(e)
            return

    # 清空文本
    def text_clear(self):
        self.editor.clear()

    # 打开显示文本
    def text_on(self):
        self.text_en = True
        self.key_text_switch.setIcon(QIcon(":/images/text_on_icon.png"))
        self.key_text_switch.disconnect()
        self.key_text_switch.clicked.connect(lambda: self.text_off())

    # 关闭显示文本
    def text_off(self):
        self.text_en = False
        self.key_text_switch.setIcon(QIcon(":/images/text_off_icon.png"))
        self.key_text_switch.disconnect()
        self.key_text_switch.clicked.connect(lambda: self.text_on())

    # 打开com
    def com_open(self):
        # 如果没有选择串口，立即返回
        if self.com_now is None:
            return

        try:
            self.com_opt_obj = serial.Serial(self.com_now.device, self.com_baudrate, timeout=0)
            self.key_com.setDisabled(True)
            self.key_baud.setDisabled(True)
            self.key_ch.setDisabled(True)
            self.key_com_switch.setIcon(QIcon(":/images/open_icon.png"))
            self.key_com_switch.disconnect()
            self.key_com_switch.clicked.connect(lambda: self.com_close())
            self.clear_all()
        except Exception as e:
            print(e)
            return

    # 关闭com
    def com_close(self):
        # 如果没有打开串口，立即返回
        if self.com_opt_obj is None:
            return

        self.com_opt_obj.close()
        self.com_opt_obj = None
        self.key_com_switch.setIcon(QIcon(":/images/close_icon.png"))
        self.key_com_switch.disconnect()
        self.key_com_switch.clicked.connect(lambda: self.com_open())
        self.key_com.setEnabled(True)
        self.key_baud.setEnabled(True)
        self.key_ch.setEnabled(True)

    # 刷新com列表
    def com_refresh(self):
        # 相关配置恢复默认
        self.com_now = None
        self.com_opt_obj = None
        self.com_action_list.clear()
        self.menu_com.clear()
        self.com_list.clear()
        # 更新串口列表
        self.com_list = list(serial.tools.list_ports.comports())  # 扫描串口
        for i in range(0, len(self.com_list)):  # 把所有串口信息添加到串口列表
            action_com = MenuAction(str(self.com_list[i].device), self.menu_com)
            self.com_action_list.append(action_com)
            self.menu_com.addAction(self.com_action_list[i])
        # 默认刷新后选择第一个串口
        if (self.com_now is None) and (self.com_list != []):
            self.com_select(self.com_list[0])
        # 最后添加刷新选项到菜单
        action_com_refresh = QAction(QIcon(":/images/refresh_icon.png"), "刷新", self.menu_com)
        action_com_refresh.triggered.connect(lambda: self.com_refresh())
        self.menu_com.addAction(action_com_refresh)

    # 选择当前的com口
    def com_select(self, com):
        self.com_now = com
        self.key_com.setText(self.com_now.device)

    # 查询com列表的点击事件
    def com_action_refresh(self):
        if self.com_opt_obj is not None:
            return

        for i in range(0, len(self.com_action_list)):
            # 如果没被按下，继续查询下一项
            if self.com_action_list[i].is_clicked == 0:
                continue
            # 否则执行对应操作并退出
            self.com_action_list[i].click_event_clear()
            self.com_select(self.com_list[i])
            break

    # 设置当前com口的波特率
    def com_set_baudrate(self, baudrate):
        self.com_baudrate = baudrate
        self.key_baud.setText(str(baudrate))

    def com_read(self):
        # 如果没有打开串口或者串口没有数据，立即返回
        if (self.com_opt_obj is None) or (self.com_opt_obj.in_waiting == 0):
            self.com_buf = b''
            return
        # 读取串口数据
        self.com_buf = self.com_opt_obj.read(self.com_opt_obj.in_waiting)

    # 刷新图像
    def graph_refresh(self):
        if self.graph_en is not True:
            return

        vector_y = list(self.com_buf)
        self.graph_y.extend(vector_y)
        len_y = len(self.graph_y)
        if len_y > self.max_len_x:
            del self.graph_y[0: len_y - self.max_len_x]

        if self.ch_num == 1:
            self.graph_ch1_y.clear()
            self.graph_ch1_y = list(self.graph_y)
            ch1_x = range(0, len(self.graph_ch1_y))
            self.curve0.setData(ch1_x, self.graph_ch1_y)

        elif self.ch_num == 2:
            self.graph_ch1_y.clear()
            self.graph_ch1_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch1_y)):
                self.graph_ch1_y[i] = self.graph_ch1_y[i] & 15
            ch1_x = range(0, len(self.graph_ch1_y))
            self.curve0.setData(ch1_x, self.graph_ch1_y)

            self.graph_ch2_y.clear()
            self.graph_ch2_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch2_y)):
                self.graph_ch2_y[i] = (self.graph_ch2_y[i] & 240) / 16 + 16 + 16
            ch1_x = range(0, len(self.graph_ch2_y))
            self.curve1.setData(ch1_x, self.graph_ch2_y)

        elif self.ch_num == 4:
            self.graph_ch1_y.clear()
            self.graph_ch1_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch1_y)):
                self.graph_ch1_y[i] = self.graph_ch1_y[i] & 3
            ch1_x = range(0, len(self.graph_ch1_y))
            self.curve0.setData(ch1_x, self.graph_ch1_y)

            self.graph_ch2_y.clear()
            self.graph_ch2_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch2_y)):
                self.graph_ch2_y[i] = (self.graph_ch2_y[i] & 12) / 4 + 8
            ch2_x = range(0, len(self.graph_ch2_y))
            self.curve1.setData(ch2_x, self.graph_ch2_y)

            self.graph_ch3_y.clear()
            self.graph_ch3_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch3_y)):
                self.graph_ch3_y[i] = (self.graph_ch3_y[i] & 48) / 16 + 8 * 2
            ch3_x = range(0, len(self.graph_ch3_y))
            self.curve2.setData(ch3_x, self.graph_ch3_y)

            self.graph_ch4_y.clear()
            self.graph_ch4_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch4_y)):
                self.graph_ch4_y[i] = (self.graph_ch4_y[i] & 192) / 64 + 8 * 3
            ch4_x = range(0, len(self.graph_ch4_y))
            self.curve3.setData(ch4_x, self.graph_ch4_y)

        elif self.ch_num == 8:
            self.graph_ch1_y.clear()
            self.graph_ch1_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch1_y)):
                self.graph_ch1_y[i] = self.graph_ch1_y[i] & 1
            ch1_x = range(0, len(self.graph_ch1_y))
            self.curve0.setData(ch1_x, self.graph_ch1_y)

            self.graph_ch2_y.clear()
            self.graph_ch2_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch2_y)):
                self.graph_ch2_y[i] = (self.graph_ch2_y[i] & 2) / 2 + 2
            ch2_x = range(0, len(self.graph_ch2_y))
            self.curve1.setData(ch2_x, self.graph_ch2_y)

            self.graph_ch3_y.clear()
            self.graph_ch3_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch3_y)):
                self.graph_ch3_y[i] = (self.graph_ch3_y[i] & 4) / 4 + 2 * 2
            ch3_x = range(0, len(self.graph_ch3_y))
            self.curve2.setData(ch3_x, self.graph_ch3_y)

            self.graph_ch4_y.clear()
            self.graph_ch4_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch4_y)):
                self.graph_ch4_y[i] = (self.graph_ch4_y[i] & 8) / 8 + 2 * 3
            ch4_x = range(0, len(self.graph_ch4_y))
            self.curve3.setData(ch4_x, self.graph_ch4_y)

            self.graph_ch5_y.clear()
            self.graph_ch5_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch5_y)):
                self.graph_ch5_y[i] = (self.graph_ch5_y[i] & 16) / 16 + 2 * 4
            ch5_x = range(0, len(self.graph_ch5_y))
            self.curve4.setData(ch5_x, self.graph_ch5_y)

            self.graph_ch6_y.clear()
            self.graph_ch6_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch6_y)):
                self.graph_ch6_y[i] = (self.graph_ch6_y[i] & 32) / 32 + 2 * 5
            ch6_x = range(0, len(self.graph_ch6_y))
            self.curve5.setData(ch6_x, self.graph_ch6_y)

            self.graph_ch7_y.clear()
            self.graph_ch7_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch7_y)):
                self.graph_ch7_y[i] = (self.graph_ch7_y[i] & 64) / 64 + 2 * 6
            ch7_x = range(0, len(self.graph_ch7_y))
            self.curve6.setData(ch7_x, self.graph_ch7_y)

            self.graph_ch8_y.clear()
            self.graph_ch8_y = list(self.graph_y)
            for i in range(0, len(self.graph_ch8_y)):
                self.graph_ch8_y[i] = (self.graph_ch8_y[i] & 128) / 128 + 2 * 7
            ch8_x = range(0, len(self.graph_ch8_y))
            self.curve7.setData(ch8_x, self.graph_ch8_y)

    # 刷新所有数据
    def refresh(self):
        # 查询com列表动作
        self.com_action_refresh()
        # 读串口数据
        self.com_read()
        # 更新文本
        self.text_refresh()
        # 更新示波器图像
        self.graph_refresh()

    # 设置通道数量
    def graph_set_ch_num(self, num):
        self.graph_clear()
        self.ch_num = num
        self.key_ch.setText("  " + str(self.ch_num))

    # 清除显示
    def clear_all(self):
        self.graph_clear()
        self.text_clear()


if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(":/images/window_icon.png"))
    window = Window()
    window.show()
    app.exec_()
