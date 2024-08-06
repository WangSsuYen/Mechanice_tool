import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Yang Iron Mechanics Tool')

        # 创建一个面板来包含所有内容
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # 黑色

        # 创建布局管理器
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建侧边菜单面板
        self.side_menu_panel = wx.Panel(self.panel, size=(200, -1))
        self.side_menu_panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色
        self.side_menu_panel.SetMinSize((200, -1))

        # 创建侧边菜单的布局管理器
        self.side_menu_sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建标签并设置字体
        self.toggle_label = wx.StaticText(self.side_menu_panel, label='Menu', size=(200, 50))
        self.toggle_label.SetBackgroundColour(wx.Colour(212, 255, 0))  # 背景颜色
        self.toggle_label.SetForegroundColour(wx.Colour(0, 0, 0))  # 字体颜色
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)  # 设置字体样式
        self.toggle_label.SetFont(font)

        # 使用 BoxSizer 来置中
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer.Add(self.toggle_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)  # 调整边距

        # 将标签的 sizer 设置为侧边菜单的 sizer
        self.side_menu_panel.SetSizer(label_sizer)

        # 将侧边菜单面板添加到侧边菜单 sizer 中
        self.side_menu_sizer.Add(self.side_menu_panel, 0, wx.EXPAND | wx.ALL, 5)

        # 创建菜单项面板
        self.menu_items_panel = wx.Panel(self.side_menu_panel)
        self.menu_items_panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色
        self.menu_items_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加菜单项
        self.formulas = ['公式 1', '公式 2', '公式 3']
        for formula in self.formulas:
            btn = wx.Button(self.menu_items_panel, label=formula)
            btn.Bind(wx.EVT_BUTTON, self.on_formula_selected)
            self.menu_items_sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 5)

        self.menu_items_panel.SetSizer(self.menu_items_sizer)
        self.side_menu_sizer.Add(self.menu_items_panel, 1, wx.EXPAND)

        # 设置侧边菜单面板的 sizer
        self.side_menu_panel.SetSizer(self.side_menu_sizer)

        # 创建内容面板
        self.content_panel = wx.Panel(self.panel)
        self.content_panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # 黑色
        self.content_panel.SetSizer(self.content_sizer)  # 设置内容面板的布局管理器

        # 创建图片面板
        self.image_panel = wx.Panel(self.content_panel)
        self.image_panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色

        # 加载并显示图片
        try:
            self.image = wx.Image('images/Bearing.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()  # 载入图片
            self.image_ctrl = wx.StaticBitmap(self.image_panel, bitmap=self.image)

            # 创建一个布局管理器来处理图片面板内的布局
            image_sizer = wx.BoxSizer(wx.HORIZONTAL)
            image_sizer.Add(self.image_ctrl, 0, wx.EXPAND | wx.ALL, 5)
            self.image_panel.SetSizer(image_sizer)

            self.content_sizer.Add(self.image_panel, 0, wx.EXPAND | wx.ALL, 5)
        except Exception as e:
            print(f"Error loading image: {e}")

        # 创建 GridSizer 用于显示多个输入框
        self.grid_sizer = wx.GridSizer(rows=3, cols=2, hgap=5, vgap=5)  # 3 行 2 列，水平和垂直间距为 5 像素

        # 添加 6 个输入框
        self.input_boxes = []
        for _ in range(6):
            text_ctrl = wx.TextCtrl(self.content_panel, size=(200, 30))
            self.grid_sizer.Add(text_ctrl, 0, wx.EXPAND | wx.ALL)
            self.input_boxes.append(text_ctrl)

        self.content_sizer.Add(self.grid_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 提交按钮
        self.submit_button = wx.Button(self.content_panel, label='提交')
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.content_sizer.Add(self.submit_button, 0, wx.CENTER | wx.ALL, 5)

        # 将面板添加到主布局管理器
        self.main_sizer.Add(self.side_menu_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.content_panel, 1, wx.EXPAND | wx.ALL, 5)

        # 设置布局管理器和布局
        self.panel.SetSizer(self.main_sizer)
        self.Fit()  # 自动调整主框架大小以适应内容
        self.Center()

    def on_formula_selected(self, event):
        formula = event.GetEventObject().GetLabel()
        wx.MessageBox(f'选择了: {formula}', '信息', wx.OK | wx.ICON_INFORMATION)

    def on_submit(self, event):
        # 获取每个输入框的值
        input_values = [box.GetValue() for box in self.input_boxes]
        wx.MessageBox(f'您输入的内容: {", ".join(input_values)}', '信息', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()