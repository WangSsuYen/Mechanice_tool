import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Yang Iron Mechanics Tool')

        # 創建一個面板來包含所有內容
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # 黑色

        # 創建佈局管理器
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)

        # 創建側邊選單面板
        self.side_menu_panel = wx.Panel(panel, size=(200, -1))
        self.side_menu_panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色
        self.side_menu_panel.SetMinSize((200, -1))

        # 創建側邊選單的佈局管理器
        self.side_menu_sizer = wx.BoxSizer(wx.VERTICAL)

        # 將按鈕更改為標籤
        self.menu_label = wx.StaticText(self.side_menu_panel, label='Menu', size=(200, 50))
        self.menu_label.SetForegroundColour(wx.Colour(255, 255, 255))  # 白色文本
        self.menu_label.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色背景

        # 將標籤添加到側邊選單
        self.side_menu_sizer.Add(self.menu_label, 0, wx.EXPAND | wx.ALL, 5)  # 調整邊距

        # 創建菜單項目面板
        self.menu_items_panel = wx.Panel(self.side_menu_panel)
        self.menu_items_panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色
        self.menu_items_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加菜單項目
        self.formulas = ['公式 1', '公式 2', '公式 3']
        for formula in self.formulas:
            btn = wx.Button(self.menu_items_panel, label=formula)
            btn.Bind(wx.EVT_BUTTON, self.on_formula_selected)
            self.menu_items_sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 5)

        self.menu_items_panel.SetSizer(self.menu_items_sizer)
        self.side_menu_sizer.Add(self.menu_items_panel, 1, wx.EXPAND)
        self.side_menu_panel.SetSizer(self.side_menu_sizer)

        # 創建內容面板
        self.content_panel = wx.Panel(panel)
        self.content_panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # 黑色
        self.content_panel.SetSizer(self.content_sizer)  # 設置內容面板的佈局管理器

        # 創建圖片面板
        self.image_panel = wx.Panel(self.content_panel)
        self.image_panel.SetBackgroundColour(wx.Colour(50, 50, 50))  # 深灰色

        # 加載並顯示圖片
        self.image = wx.Image('images/Bearing.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()  # 載入圖片
        self.image_ctrl = wx.StaticBitmap(self.image_panel, bitmap=self.image)

        # 創建一個佈局管理器來處理圖片面板內的佈局
        image_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_sizer.Add(self.image_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        self.image_panel.SetSizer(image_sizer)

        self.content_sizer.Add(self.image_panel, 0, wx.EXPAND | wx.ALL, 5)

        # 創建 GridSizer 用於顯示多個輸入框
        self.grid_sizer = wx.GridSizer(rows=3, cols=2, hgap=5, vgap=5)  # 3 行 2 列，水平和垂直間距為 5 像素

        # 添加 6 個輸入框
        for _ in range(6):
            text_ctrl = wx.TextCtrl(self.content_panel, size=(200, 30))
            self.grid_sizer.Add(text_ctrl, 0, wx.EXPAND | wx.ALL)

        self.content_sizer.Add(self.grid_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 提交按鈕
        self.submit_button = wx.Button(self.content_panel, label='提交')
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.content_sizer.Add(self.submit_button, 0, wx.CENTER | wx.ALL, 5)

        # 將面板添加到主佈局管理器
        self.main_sizer.Add(self.side_menu_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.content_panel, 1, wx.EXPAND | wx.ALL, 5)

        # 設置佈局管理器和佈局
        panel.SetSizer(self.main_sizer)
        self.Fit()  # 自動調整主框架大小以適應內容
        self.Center()

    def on_formula_selected(self, event):
        formula = event.GetEventObject().GetLabel()
        wx.MessageBox(f'選擇了: {formula}', '資訊', wx.OK | wx.ICON_INFORMATION)

    def on_submit(self, event):
        input_value = self.input_box.GetValue()
        wx.MessageBox(f'您輸入的內容: {input_value}', '資訊', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
