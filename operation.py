import wx

# 螺桿推力計算
class ScrewThrustPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 畫欄位
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        # 添加圖片格子
        image = wx.Image('images/Bearing.jpg', wx.BITMAP_TYPE_JPEG)
        image = image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(image))
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 畫輸入欄位
        form_sizer = wx.GridSizer(cols=2, vgap=30, hgap=30)
        sizer.Add(form_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 新增欄位
        self.AddLabeledTextCtrl(form_sizer, '馬達力矩：', "N.m")
        self.AddLabeledTextCtrl(form_sizer, "螺桿直徑：", 'mm')
        self.AddLabeledTextCtrl(form_sizer, "螺桿導程：", "mm")
        self.AddLabeledTextCtrl(form_sizer, "導程角：", 'Deg')
        self.AddLabeledTextCtrl(form_sizer, "損失估算：", "%")

        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(80, 70, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)
        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255,0,0))
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)


    def AddLabeledTextCtrl(self, sizer, label, unit):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 抬頭
        lbl = wx.StaticText(self, label=label, size=(80,20))
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 輸入框
        txt = wx.TextCtrl(self, size=(100,20))
        box.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 單位
        unit_lbl = wx.StaticText(self, label=unit)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 添加到主布局
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

# 皮帶計算
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

# 流體力學計算
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
