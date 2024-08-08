import wx


# 側邊細項
class SideMenu(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.size = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.size)
        self.SetBackgroundColour(wx.Colour(0, 255, 255))

        self.menu_items_panel = wx.Panel(self)
        self.menu_items_sizer = wx.BoxSizer(wx.VERTICAL)
        self.menu_items_panel.SetSizer(self.menu_items_sizer)

        self.size.Add(self.menu_items_panel, 1, wx.EXPAND | wx.ALL, 10)

        self.menu_item()

    # 力學細項
    def menu_item(self):
        # 添加菜單項目
        self.formulas = ['螺桿推力', '皮帶', '流速流量計算', '斜角滾珠軸承', '滾針軸承']
        for formula in self.formulas:
            btn = wx.Button(self.menu_items_panel, label=formula)
            btn.Bind(wx.EVT_BUTTON, self.on_formula_selected)
            self.menu_items_sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 5)

    def on_formula_selected(self, event):
        # 在此處添加按鈕點擊事件處理程式碼
        button = event.GetEventObject()
        label = button.GetLabel()
        wx.MessageBox(f'您選擇了: {label}', '信息', wx.OK | wx.ICON_INFORMATION)


# 主畫面
class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.size = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.SetSizer(self.size)

        self.side_menu = SideMenu(self.panel)
        self.main_content = wx.Panel(self.panel)

        self.size.Add(self.side_menu, 0, wx.EXPAND | wx.ALL, 5)
        self.size.Add(self.main_content, 1, wx.EXPAND | wx.ALL, 5)

        self.SetTitle('Yang Iron Mechanice Tools')
        self.SetSize((800, 600))
        self.Centre()


if __name__ == '__main__':
    app = wx.App(redirect=True, useBestVisual=True)
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()