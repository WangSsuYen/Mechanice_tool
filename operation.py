import wx, math
from data import *

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
        self.motor_torque = self.AddLabeledTextCtrl(grid_sizer, '馬達力矩：', "N.m", 90, 20)
        self.screw_diameter = self.AddLabeledTextCtrl(grid_sizer, "螺桿直徑：", 'mm', 90, 20)
        self.screw_pitch = self.AddLabeledTextCtrl(grid_sizer, "螺桿導程：", "mm", 90, 20)
        self.power_lossed = self.AddLabeledTextCtrl(grid_sizer, "損失估算：", "%", 90, 20)

        # 設定輸出欄位
        output_form = wx.GridSizer(cols=2, vgap=30, hgap=30)
        sizer.Add(output_form, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        self.screw_degress = self.AddLabeledTextCtrl(output_form, "導程角：", "Deg", 70, 20, readonly=True)
        self.total_power = self.AddLabeledTextCtrl(output_form, "總輸出：", "N", 70, 20, readonly=True)

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
    def AddLabeledTextCtrl(self, sizer, label, unit, width, high, readonly=False):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 抬頭
        lbl = wx.StaticText(self, label=label, size=(width, high))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl.SetFont(font)
        # 單位
        unit_lbl = wx.StaticText(self, label=unit)
        # 確認是否為唯獨
        if readonly :
            style = wx.TE_READONLY
            lbl.SetForegroundColour(wx.Colour(255,255,240))
            unit_lbl.SetForegroundColour(wx.Colour(255,255,240))
        else:
            style = 0
        # 輸入框
        txt = wx.TextCtrl(self, size=(100, 20), style=style)
        # 加入畫面
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
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
        fixed_size = wx.Size(1200,-1)

        # 第一階段運算畫面
        first_level_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="第一階段運算"), wx.VERTICAL)
        first_font = wx.Font(25, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        first_level_bg.GetStaticBox().SetFont(first_font)
        first_level_bg.GetStaticBox().SetForegroundColour(wx.Colour(0,0,255))
        sizer.Add(first_level_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Ko負荷補正係數
        # 框
        Ko_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="負荷補正係數(Ko)"), wx.HORIZONTAL)
        Ko_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        Ko_bg.GetStaticBox().SetFont(Ko_font)
        Ko_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        Ko_bg.GetStaticBox().SetMinSize(fixed_size)
        # 圖片示意
        Ko_image = wx.Image('images/Ko.png', wx.BITMAP_TYPE_PNG)
        Ko_image = Ko_image.Scale(800, 300, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(Ko_image))
        # 加入圖框
        Ko_bg.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 欄位
        self.Ko = self.AddLabeledTextCtrl(Ko_bg, "負荷補正係數(Ko) : ", "", 150, 20)
        first_level_bg.Add(Ko_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # Ki惰輪修正係數
        # 框
        Ki_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="惰輪修正係數(Ki)"), wx.HORIZONTAL)
        Ki_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        Ki_bg.GetStaticBox().SetFont(Ki_font)
        Ki_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        Ki_bg.GetStaticBox().SetMinSize(fixed_size)
        # 圖片示意
        Ki_image = wx.Image('images/Ki.png', wx.BITMAP_TYPE_PNG)
        Ki_image = Ki_image.Scale(800, 300, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(Ki_image))
        # 加入圖框
        Ki_bg.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 欄位
        self.Ki = self.AddLabeledTextCtrl(Ki_bg, "惰輪補正係數(Ki) : ", "", 150, 20)
        first_level_bg.Add(Ki_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # Ke環境補正係數
        # 框
        Ke_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="環境補正係數(Ke)"), wx.HORIZONTAL)
        Ke_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        Ke_bg.GetStaticBox().SetFont(Ke_font)
        Ke_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        Ke_bg.GetStaticBox().SetMinSize(fixed_size)
        # 圖片示意
        Ke_image = wx.Image('images/Ke.png', wx.BITMAP_TYPE_PNG)
        Ke_image = Ke_image.Scale(800, 300, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(Ke_image))
        # 加入圖框
        Ke_bg.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 欄位
        self.Ke = self.AddLabeledTextCtrl(Ke_bg, "環境補正係數(Ke) : ", "", 150, 20)
        first_level_bg.Add(Ke_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # 設計動力
        power_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="設計動力(Pd)"), wx.HORIZONTAL)
        power_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        power_bg.GetStaticBox().SetFont(power_font)
        power_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        power_bg.GetStaticBox().SetMinSize(fixed_size)
        power_sizer = wx.GridSizer(cols=2, vgap=10, hgap=100)
        self.motor_torque = self.AddLabeledTextCtrl(power_sizer, "傳輸動力(Pt) : ", "Kw", 120, 20)
        self.design_torque = self.AddLabeledTextCtrl(power_sizer, "設計動力(Pd) : ", "Kw", 120, 20, readonly=True)
        power_bg.Add(power_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        first_level_bg.Add(power_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # 皮帶輪有效直徑
        pulley_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="皮帶輪計算"), wx.HORIZONTAL)
        pulley_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        pulley_bg.GetStaticBox().SetFont(pulley_font)
        pulley_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        pulley_bg.GetStaticBox().SetMinSize(fixed_size)
        pulley_sizer = wx.GridSizer(cols=3, vgap=10, hgap=50)
        self.motor_pulley_diameter = self.AddLabeledTextCtrl(pulley_sizer, "馬達皮帶輪有效直徑 : ", "mm", 170, 20)
        self.motor_RPM = self.AddLabeledTextCtrl(pulley_sizer, "馬達轉速 : ", "RPM", 80, 20)
        self.spindle_RPM = self.AddLabeledTextCtrl(pulley_sizer, "主軸轉速 : ", "RPM", 80, 20)
        self.spindle_pulley_diameter = self.AddLabeledTextCtrl(pulley_sizer, "主軸皮帶輪有效直徑 : ", "mm", 170, 20, readonly=True)
        pulley_bg.Add(pulley_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        first_level_bg.Add(pulley_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # 求皮帶長度
        belt_length_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="求皮帶長度"), wx.HORIZONTAL)
        belt_length_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        belt_length_bg.GetStaticBox().SetFont(belt_length_font)
        belt_length_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        belt_length_bg.GetStaticBox().SetMinSize(fixed_size)
        belt_length_sizer = wx.GridSizer(cols=3, vgap=10, hgap=100)
        self.distance_between_pulley = self.AddLabeledTextCtrl(belt_length_sizer, "皮帶輪中心距 : ", "mm", 120, 20)
        self.belt_perimeter = self.AddLabeledTextCtrl(belt_length_sizer, "皮帶周長 : ", "mm", 90, 20, readonly=True)
        self.belt_contact_degress = self.AddLabeledTextCtrl(belt_length_sizer, "接觸角 :  : ", "°", 90, 20, readonly=True)
        belt_length_bg.Add(belt_length_sizer, 0 ,wx.ALIGN_CENTER | wx.ALL , 10)
        first_level_bg.Add(belt_length_bg, 0 ,wx.ALIGN_CENTER | wx.ALL , 10)


        # 皮帶建議
        belt_selection_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="建議皮帶使用"), wx.HORIZONTAL)
        belt_selection_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        belt_selection_bg.GetStaticBox().SetFont(belt_selection_font)
        belt_selection_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        belt_selection_bg.GetStaticBox().SetMinSize(fixed_size)
        # 圖片示意
        belt_selection_image = wx.Image('images/belt_selection.jpg', wx.BITMAP_TYPE_JPEG)
        belt_selection_image = belt_selection_image.Scale(800, 300, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(belt_selection_image))
        # 加入圖框
        belt_selection_bg.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.belt_selection = self.AddLabeledTextCtrl(belt_selection_bg, "建議使用皮帶 : ", "", 120, 20, readonly=True)
        first_level_bg.Add(belt_selection_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # Kθ接觸角係數
        Kθ_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="Kθ接觸角係數"), wx.HORIZONTAL)
        Kθ_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        Kθ_bg.GetStaticBox().SetFont(Kθ_font)
        Kθ_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        Kθ_bg.GetStaticBox().SetMinSize(fixed_size)
        # 圖片示意
        Kθ_image = wx.Image('images/Kθ.jpg', wx.BITMAP_TYPE_JPEG)
        Kθ_image = Kθ_image.Scale(800, 300, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(Kθ_image))
        # 加入圖框
        Kθ_bg.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 欄位
        self.Kθ = self.AddLabeledTextCtrl(Kθ_bg, "接觸角補正係數(Kθ) : ", "", 160, 20, readonly=True)
        first_level_bg.Add(Kθ_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # Kl長度補正係數
        Kl_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="Kl長度補正係數"), wx.HORIZONTAL)
        Kl_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        Kl_bg.GetStaticBox().SetFont(Kl_font)
        Kl_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        Kl_bg.GetStaticBox().SetMinSize(fixed_size)
        # 圖片示意
        Kl_image = wx.Image('images/Kl.jpg', wx.BITMAP_TYPE_JPEG)
        Kl_image = Kl_image.Scale(300, 800, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(Kl_image))
        # 加入圖框
        Kl_bg.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        # 欄位
        self.Kl = self.AddLabeledTextCtrl(Kl_bg, "長度補正係數(Kθ) : ", "", 160, 20, readonly=True)
        first_level_bg.Add(Kl_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Kc容量補正及皮帶用量
        Kc_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="輸出"), wx.HORIZONTAL)
        Kc_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        Kc_bg.GetStaticBox().SetFont(Kc_font)
        Kc_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        Kc_bg.GetStaticBox().SetMinSize(fixed_size)
        Kc_sizer = wx.GridSizer(cols=2, vgap=10, hgap=100)
        self.pc_value = self.AddLabeledTextCtrl(Kc_sizer, "補正運動容量 : ", "Kw", 100, 20, readonly=True)
        self.belt_count = self.AddLabeledTextCtrl(Kc_sizer, "皮帶用量 : ", "條", 80, 20, readonly=True)
        Kc_bg.Add(Kc_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        first_level_bg.Add(Kc_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)

        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.expression)
        first_level_bg.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 10)


        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(20, 20)  # 設置滾動速率

    # 欄位新增器
    def AddLabeledTextCtrl(self, sizer, label, unit, label_width, label_high, readonly=False):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 抬頭
        lbl = wx.StaticText(self, label=label, size=(label_width, label_high))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl.SetFont(font)
        # 單位
        unit_lbl = wx.StaticText(self, label=unit)
         # 確認是否為唯獨
        if readonly :
            style = wx.TE_READONLY
            lbl.SetForegroundColour(wx.Colour(255,255,240))
            unit_lbl.SetForegroundColour(wx.Colour(255,255,240))
        else:
            style = 0
        # 輸入欄
        txt = wx.TextCtrl(self, size=(100, 20), style=style)
        # 加入畫面
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # 添加到主布局
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)
        return txt


    # 運算式
    def expression(self, event):
        datas = read_excel()
        try:
            Ko = float(self.Ko.GetValue())
            Ki = float(self.Ki.GetValue())
            Ke = float(self.Ke.GetValue())
            # 馬達動力
            motor_torque = float(self.motor_torque.GetValue())
            # 馬達皮帶輪直徑
            motor_pulley_diameter = float(self.motor_pulley_diameter.GetValue())
            # 馬達轉速
            motor_RPM = float(self.motor_RPM.GetValue())
            # 主軸轉速
            spindle_RPM = float(self.spindle_RPM.GetValue())
            # 皮帶輪間距
            distance_between_pulley = float(self.distance_between_pulley.GetValue())
            # 設計動力
            design_torque = float(round(motor_torque * (Ko + Ki + Ke), 2))
            # 主軸皮帶直徑
            spindle_pulley_diameter = float(round(motor_pulley_diameter / spindle_RPM * motor_RPM ,2))
            # 皮帶周長
            belt_perimeter = float(round(2 * distance_between_pulley + ((motor_pulley_diameter + spindle_pulley_diameter) * 1.57554),2))
            # 皮帶接觸角
            belt_contact_degress = float(round(180 - ((math.asin(abs(motor_pulley_diameter - spindle_pulley_diameter) / distance_between_pulley) * 180 / math.pi) * 2),2))
            # 皮帶選擇
            belt_selection = datas.belt_selection(motor_RPM,design_torque)
            # Kθ的值
            Kθ_value = datas.Kθ_value(belt_contact_degress)
            # Kl值
            Kl_value = datas.Kl_value(distance_between_pulley, belt_selection)
            # Kc運動容量補正係數
            rotation_container_coefficient = float(round(Kθ_value * Kl_value, 2))
            # Ps基準運動動力(Kw)
            ps_value = datas.ps_value(belt_selection, spindle_RPM, spindle_pulley_diameter)
            # Pa迴轉比附加動力(Kw)
            pa_value = datas.pa_value(belt_selection, spindle_RPM, motor_RPM)
            # Pc運動容量補正(Kw)
            pc_value = round((ps_value + pa_value) * rotation_container_coefficient, 2)
            # 皮帶使用數量
            belt_count = math.ceil(design_torque / pc_value)



            # 設計動力運算
            self.design_torque.SetValue(f"{design_torque}")
            # 主軸皮帶倫有效直徑運算
            self.spindle_pulley_diameter.SetValue(f"{spindle_pulley_diameter}")
            # 皮帶周長計算
            self.belt_perimeter.SetValue(f"{belt_perimeter}")
            # 皮帶建議
            self.belt_selection.SetValue(f"{belt_selection}")
            # 接觸角運算
            self.belt_contact_degress.SetValue(f"{belt_contact_degress}")
            # Kθ值
            self.Kθ.SetValue(f"{Kθ_value}")
            # Kl值
            self.Kl.SetValue(f"{Kl_value}")
            # Pc值
            self.pc_value.SetValue(f"{pc_value}")
            # 皮帶使用數量
            self.belt_count.SetValue(f"{belt_count}")


        except ValueError:
            wx.MessageBox('請輸入有效的數字', '錯誤', wx.OK | wx.ICON_ERROR)



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
