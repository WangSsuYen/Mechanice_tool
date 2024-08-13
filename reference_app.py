import wx, traceback
from operation import ScrewThrustPanel, fiveV_BeltPanel, FluidMechanicsPanel


# 側畫面
class SideMenu(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_frame = parent.GetParent()  # 獲取主框架的引用
        self.InitUI()

    def InitUI(self):
        # 背景、視窗大小設定
        self.SetBackgroundColour(wx.Colour(0, 255, 255))
        self.SetMinSize((200, 0))

        # 視窗管理器
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # 抬頭背景設定
        self.titel_bgc = wx.Panel(self)
        self.titel_bgc.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.sizer.Add(self.titel_bgc, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # 抬頭的佈局管理器
        self.title_sizer = wx.BoxSizer(wx.VERTICAL)
        self.titel_bgc.SetSizer(self.title_sizer)

        # 抬頭設定
        self.title = wx.StaticText(self.titel_bgc, label="力學計算機", size=(200,60))
        self.title.SetForegroundColour(wx.Colour(255, 255, 255))
        font = wx.Font(25, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.title.SetFont(font)
        self.title_sizer.Add(self.title, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.formulas = ['螺桿推力', '5V型皮帶', '流體力學']
        for formula in self.formulas:
            btn = wx.Button(self, label=formula)
            btn.Bind(wx.EVT_BUTTON, self.OnFormulaSelected)
            self.sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 10)

    def OnFormulaSelected(self, event):
        button = event.GetEventObject()
        label = button.GetLabel()
        self.main_frame.SwitchPanel(label)  # 呼叫主框架的 SwitchPanel 方法


# 主畫面
class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        # 主畫面管理器
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.SetSizer(self.sizer)

        # 側邊欄位規劃
        self.side_menu = SideMenu(self.panel)
        self.sizer.Add(self.side_menu, 0, wx.EXPAND | wx.ALL, 5)

        # 主畫面規劃
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.main_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # 選擇主頁類別
        self.screw_thrust_panel = ScrewThrustPanel(self.panel)
        self.fiveV_BeltPanel = fiveV_BeltPanel(self.panel)
        self.fluid_mechanics_panel = FluidMechanicsPanel(self.panel)

        # 類別匯入主頁
        self.main_sizer.Add(self.screw_thrust_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.fiveV_BeltPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.fluid_mechanics_panel, 1, wx.EXPAND | wx.ALL, 5)

        # 其他類別隱藏
        self.screw_thrust_panel.Hide()
        self.fiveV_BeltPanel.Hide()
        self.fluid_mechanics_panel.Hide()

        self.SetTitle('Yang Iron Mechanice Tools')
        self.Maximize(True)
        self.Centre()

    def SwitchPanel(self, label):
        self.screw_thrust_panel.Hide()
        self.fiveV_BeltPanel.Hide()
        self.fluid_mechanics_panel.Hide()

        if label == '螺桿推力':
            self.screw_thrust_panel.Show()
        elif label == '5V型皮帶':
            self.fiveV_BeltPanel.Show()
        elif label == '流體力學':
            self.fluid_mechanics_panel.Show()

        self.panel.Layout()



if __name__ == '__main__':
    try:
        app = wx.App(False)
        frame = MainFrame(None)
        frame.Show()
        app.MainLoop()
    except Exception as e:
        error_message = traceback.format_exc()
        wx.MessageBox(f"程序出現異常:\n\n{error_message}", "錯誤", wx.OK | wx.ICON_ERROR)
