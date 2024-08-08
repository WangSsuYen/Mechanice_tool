import wx

class ScrewThrustPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.AddLabeledTextCtrl(sizer, "馬達力矩：")
        self.AddLabeledTextCtrl(sizer, "螺桿直徑：")
        self.AddLabeledTextCtrl(sizer, "螺桿導程：")
        self.AddLabeledTextCtrl(sizer, "導程角：")
        self.AddLabeledTextCtrl(sizer, "損失估算：")

        calc_button = wx.Button(self, label="送出計算")
        sizer.Add(calc_button, 0, wx.EXPAND | wx.ALL, 5)

    def AddLabeledTextCtrl(self, sizer, label):
        box = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=label)
        txt = wx.TextCtrl(self)
        box.Add(lbl, 0, wx.ALL, 5)
        box.Add(txt, 1, wx.ALL, 5)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

class BeltPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.AddLabeledTextCtrl(sizer, "負荷補正系數：")
        self.AddLabeledTextCtrl(sizer, "加速度負荷補正系數：")
        self.AddLabeledTextCtrl(sizer, "工作時間補正系數：")
        self.AddLabeledTextCtrl(sizer, "惰輪負荷補正系數：")
        self.AddLabeledTextCtrl(sizer, "電機功率：")

        calc_button = wx.Button(self, label="送出計算")
        sizer.Add(calc_button, 0, wx.EXPAND | wx.ALL, 5)

    def AddLabeledTextCtrl(self, sizer, label):
        box = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=label)
        txt = wx.TextCtrl(self)
        box.Add(lbl, 0, wx.ALL, 5)
        box.Add(txt, 1, wx.ALL, 5)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

class FluidMechanicsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.AddLabeledTextCtrl(sizer, "流量：")
        self.AddLabeledTextCtrl(sizer, "面積：")
        self.AddLabeledTextCtrl(sizer, "壓力：")
        self.AddLabeledTextCtrl(sizer, "溫度：")

        calc_button = wx.Button(self, label="送出計算")
        sizer.Add(calc_button, 0, wx.EXPAND | wx.ALL, 5)

    def AddLabeledTextCtrl(self, sizer, label):
        box = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=label)
        txt = wx.TextCtrl(self)
        box.Add(lbl, 0, wx.ALL, 5)
        box.Add(txt, 1, wx.ALL, 5)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)
