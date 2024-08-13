import wx, math

# 螺桿推力計算
class ScrewThrustPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 主佈局使用 BoxSizer 管理元件
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # 添加圖片
        image = wx.Image('images/ScrewDrive.jpg', wx.BITMAP_TYPE_JPEG)
        image = image.Scale(1200, 450, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(image))
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 使用 StaticBoxSizer 創建輸入區域背景
        form_bg = wx.StaticBox(self, label="輸入區")
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        form_bg.SetFont(font)
        form_sizer = wx.StaticBoxSizer(form_bg, wx.VERTICAL)

        # 添加 GridSizer 作為輸入欄位的管理器
        grid_sizer = wx.GridSizer(cols=2, vgap=30, hgap=30)
        form_sizer.Add(grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # 將輸入區域加入到主佈局中
        sizer.Add(form_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

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
        btn_icon = btn_icon.Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)

        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.expression)
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 30)

        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(50, 50)  # 設置滾動速率

    # 欄位新增器
    def AddLabeledTextCtrl(self, sizer, label, unit):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 抬頭
        lbl = wx.StaticText(self, label=label, size=(90, 20))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl.SetFont(font)
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
class fiveV_BeltPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 畫面規劃
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # 主頁圖片
        image = wx.Image('images/graph.png', wx.BITMAP_TYPE_PNG)
        image = image.Scale(1200, 450, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(image))
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 輸入/輸出分隔
        in_out_sizer = wx.GridSizer(cols=2, vgap=10, hgap=10)
        in_out_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="計算區"), wx.HORIZONTAL)
        title_font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        in_out_bg.GetStaticBox().SetFont(title_font)
        in_out_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        in_out_bg.Add(in_out_sizer, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(in_out_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 數值輸入區
        input_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="輸入區"), wx.VERTICAL)
        input_title_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        input_sizer.GetStaticBox().SetFont(input_title_font)
        input_sizer.GetStaticBox().SetForegroundColour(wx.Colour(0,250,145))
        in_out_sizer.Add(input_sizer, 0 , wx.ALIGN_CENTER_VERTICAL | wx.ALL ,15)

        # 數值輸出區
        output_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="輸出區"), wx.VERTICAL)
        output_title_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        output_sizer.GetStaticBox().SetFont(output_title_font)
        output_sizer.GetStaticBox().SetForegroundColour(wx.Colour(0,250,145))
        in_out_sizer.Add(output_sizer, 0 , wx.ALIGN_CENTER_VERTICAL | wx.ALL ,15)

        # 動力設計輸入區
        input_power_setting = wx.StaticBoxSizer(wx.StaticBox(self, label="動力設計參數"), wx.VERTICAL)
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        input_power_setting.GetStaticBox().SetFont(font)
        # 動力設計欄位入
        self.motor_power = self.AddLabeledTextCtrl(input_power_setting, "馬達動力 : ", "Kw")
        input_sizer.Add(input_power_setting, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        # 皮帶計算輸入區
        input_belt_setting = wx.StaticBoxSizer(wx.StaticBox(self, label="皮帶設計參數"), wx.VERTICAL)
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        input_belt_setting.GetStaticBox().SetFont(font)
        self.belt_diameter = self.AddLabeledTextCtrl(input_belt_setting, "馬達皮帶輪有效直徑 ： ", "mm")
        self.motor_speed = self.AddLabeledTextCtrl(input_belt_setting, "馬達轉速 ： ", "RPM")
        self.spindle_spped = self.AddLabeledTextCtrl(input_belt_setting, "主軸轉速 ： ", "RPM")


        self.AddLabeledTextCtrl(input_belt_setting, "惰輪負荷補正系數：", "")
        self.AddLabeledTextCtrl(input_belt_setting, "電機功率：", "Kw")
        input_sizer.Add(input_belt_setting, 0 , wx.ALIGN_CENTER | wx.ALL, 15)

        calc_button = wx.Button(self, label="送出計算")
        sizer.Add(calc_button, 0, wx.EXPAND | wx.ALL, 5)

        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(20, 20)  # 設置滾動速率

    # 欄位新增器
    def AddLabeledTextCtrl(self, sizer, label, unit):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 抬頭
        lbl = wx.StaticText(self, label=label, size=(200, 20))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl.SetFont(font)
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
