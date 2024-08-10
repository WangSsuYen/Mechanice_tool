import wx, math


import wx
import math

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
        image = wx.Image('images/ScrewDrive.jpg', wx.BITMAP_TYPE_JPEG)
        image = image.Scale(800, 300, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(image))
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 畫輸入欄位背景
        form_bg = wx.StaticBox(self, label="輸入區", size=(200,60))
        form_bg.SetBackgroundColour(wx.Colour(0, 255, 255))
        font = wx.Font(60, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        form_bg.SetFont(font)

        # 輸入欄位管理器
        form_sizer = wx.StaticBoxSizer(form_bg, wx.VERTICAL)
        grid_sizer = wx.GridSizer(cols=2, vgap=30, hgap=30)

        # 將欄位背景加入到輸入欄位管理器
        form_sizer.Add(grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        # 將輸入欄位管理器加照主畫面裡
        sizer.Add(form_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # 設定輸入欄位
        self.motor_torque = self.AddLabeledTextCtrl(grid_sizer, '馬達力矩：', "N.m")
        self.screw_diameter = self.AddLabeledTextCtrl(grid_sizer, "螺桿直徑：", 'mm')
        self.screw_pitch = self.AddLabeledTextCtrl(grid_sizer, "螺桿導程：", "mm")
        self.power_lossed = self.AddLabeledTextCtrl(grid_sizer, "損失估算：", "%")

        # 設定輸出欄位
        output_form = wx.GridSizer(cols=2, vgap=30, hgap=30)
        sizer.Add(output_form, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        self.screw_degress = self.AddLabeledTextCtrl(output_form, "導程角：", "Deg")
        self.total_power = self.AddLabeledTextCtrl(output_form, "總輸出：", "N")

        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(80, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)
        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.expression)
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 30)

    # 欄位新增器
    def AddLabeledTextCtrl(self, sizer, label, unit):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 抬頭
        lbl = wx.StaticText(self, label=label, size=(80, 20))
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 輸入框
        txt = wx.TextCtrl(self, size=(100, 20))
        box.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 單位
        unit_lbl = wx.StaticText(self, label=unit)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 添加到主布局
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)
        return txt

    # 運算式
    def expression(self, event):
        try:
            motor_torque = float(self.motor_torque.GetValue())
            screw_diameter = float(self.screw_diameter.GetValue())
            screw_pitch = float(self.screw_pitch.GetValue())
            power_lossed = float(self.power_lossed.GetValue())

            # 計算導程角
            screw_degress = math.degrees(math.atan(screw_pitch / (screw_diameter * math.pi)))
            self.screw_degress.SetValue(f"{screw_degress:.3f}")

            # 計算總輸出
            total_output = (2 * math.pi * (1 - power_lossed / 100) * motor_torque) / (screw_pitch / 1000)
            self.total_power.SetValue(f"{total_output:.3f}")

        except ValueError:
            wx.MessageBox('請輸入有效的數字', '錯誤', wx.OK | wx.ICON_ERROR)



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
