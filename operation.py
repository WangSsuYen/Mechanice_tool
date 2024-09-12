import wx, math, wx.adv, wx.grid
from mathematical import *
from model import *
from dialog_win import *

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
        # 畫面長寬設定
        fixed_size = wx.Size(1200,-1)
        # 畫面規劃
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

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
        sizer.Add(Ko_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(Ki_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(Ke_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(power_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(pulley_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(belt_length_bg, 0 ,wx.ALIGN_CENTER | wx.ALL , 10)


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
        sizer.Add(belt_selection_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(Kθ_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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
        sizer.Add(Kl_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)

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
        sizer.Add(Kc_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)

        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.expression)
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 10)


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



# 軸承壽命估算
class bearing_lifespan(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 畫面長寬設定
        fixed_size = wx.Size(900,-1)
        # 畫面管理器
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        picture_sizer = wx.GridSizer(cols=2, vgap=10, hgap=200)
        # 添加圖片及文字
        angular_image_with_text = self.AddTextToImage('images/angular_bearing.jpg', '斜角滾珠軸承示意圖')
        angular_bitmap = wx.StaticBitmap(self, -1, angular_image_with_text)
        picture_sizer.Add(angular_bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        cylindrical_image_with_text = self.AddTextToImage('images/cylindrical_bearing.png', '滾針軸承示意圖')
        cylindrical_bitmap = wx.StaticBitmap(self, -1, cylindrical_image_with_text)
        picture_sizer.Add(cylindrical_bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        sizer.Add(picture_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

         # 添加下拉選擇欄位
        self.AddDropdown(sizer)

        # 輸入區
        bg_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="輸入區"), wx.HORIZONTAL)
        bg_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        bg_sizer.GetStaticBox().SetFont(bg_font)
        bg_sizer.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        bg_sizer.GetStaticBox().SetMinSize(fixed_size)

        # 輸入區
        input_sizer = wx.GridSizer(cols=3, vgap=10, hgap=100)
        self.dynamic_load = self.AddLabeledTextCtrl(input_sizer, "額定動負載 ：", "KN", 140, 20)
        self.bearing_dynamic_load = self.AddLabeledTextCtrl(input_sizer, "軸承當量動負載 ：", "KN", 140, 20)
        self.rpm = self.AddLabeledTextCtrl(input_sizer, "轉速 ：", "RPM", 140, 20)
        bg_sizer.Add(input_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(bg_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # 輸出區
        output_sizer = wx.GridSizer(cols=2, vgap=10, hgap=100)
        self.rpm_lifespan = self.AddLabeledTextCtrl(output_sizer, "基本額定壽命 ：", "Millions RPM", 140, 20, readonly=True)
        self.hour_lifespan = self.AddLabeledTextCtrl(output_sizer, "基本額定壽命 ：", "Hours", 140, 20, readonly=True)
        sizer.Add(output_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)

        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.expression)
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(20, 20)  # 設置滾動速率


    def AddTextToImage(self, image_path, text):
        # 加載圖片
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        # 創建畫布
        bmp = wx.Bitmap(image)
        width, height = bmp.GetSize()
        # 創建內存DC
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(bmp)
        # 設置字型
        font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        mem_dc.SetFont(font)
        # 設置文字顏色
        mem_dc.SetTextForeground(wx.Colour(255, 0, 0))  # 使用紅色字體
        # 計算文字位置
        text_width, text_height = mem_dc.GetTextExtent(text)
        x = (width - text_width) // 2  # 文字水平居中
        y = height - text_height - 10  # 文字位置從底部上方10像素
        # 繪制文字
        mem_dc.DrawText(text, x, y)
        # 清理
        mem_dc.SelectObject(wx.NullBitmap)
        # 返回帶有文字的圖片
        return bmp


    # 下拉選擇器
    def AddDropdown(self, sizer):
        # 創建下拉選擇欄位
        dropdown_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dropdown_lbl = wx.StaticText(self, label="選擇軸承滾珠類別 ： ", size=(200, 30))
        dropdown_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dropdown_lbl.SetFont(dropdown_font)
        dropdown_lbl.SetForegroundColour(wx.Colour(255,106,106))
        # 選項
        self.options = {"滾珠軸承":3, "滾子/針軸承":3.33333333}
        # 提取選項
        self.choices = list(self.options.keys())

        self.dropdown = wx.Choice(self, choices=self.choices, size=(150, 30))
        dropdown_sizer.Add(dropdown_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        dropdown_sizer.Add(self.dropdown, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(dropdown_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)


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


    def expression(self, event):
        try:
            # 獲取用戶輸入的數值
            dynamic_load = float(self.dynamic_load.GetValue())
            bearing_dynamic_load = float(self.bearing_dynamic_load.GetValue())
            rpm = float(self.rpm.GetValue())

            # 獲取選擇的選項文本
            selected_option = self.dropdown.GetStringSelection()
            # 根據選擇的選項獲取對應的係數
            coefficient = self.options.get(selected_option)

            if coefficient is None:
                raise ValueError("未選擇有效的選項")

            # 計算基本額定壽命
            rpm_lifespan = math.pow((dynamic_load / bearing_dynamic_load), coefficient)
            hour_lifespan = (rpm_lifespan * (10**6)) / (60 * rpm)

            # 顯示結果
            self.rpm_lifespan.SetValue(f"{round(rpm_lifespan, 2)}")
            self.hour_lifespan.SetValue(f"{round(hour_lifespan, 2)}")

        except ValueError as e:
            wx.MessageBox(f"輸入錯誤: {e}", "錯誤", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"計算錯誤: {e}", "錯誤", wx.OK | wx.ICON_ERROR)





# 軸承溫升估算
class bearing_temp_rise(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 畫面長寬設定
        fixed_size = wx.Size(1200,-1)
        # 畫面管理器
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        # 添加圖片及文字
        angular_image_with_text = self.MergeImage('images/angular_bearing.jpg', 'images/temperature_rise_icon.jpg')
        angular_bitmap = wx.StaticBitmap(self, -1, angular_image_with_text)
        sizer.Add(angular_bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 輸入區
        input_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="輸入區"), wx.HORIZONTAL)
        input_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        input_sizer.GetStaticBox().SetFont(input_font)
        input_sizer.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        input_sizer.GetStaticBox().SetMinSize(fixed_size)
        # 左側圖文
        text_sizer = wx.GridSizer(cols= 3, vgap=10, hgap=20)
        text_image = wx.Image('images/friction_coefficient.png', wx.BITMAP_TYPE_PNG)
        text_image = text_image.Scale(316, 462, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(text_image))
        text_sizer.Add(bitmap, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        # 中間欄位
        middel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bearing_friction_coefficient = self.AddLabeledTextCtrl(middel_sizer, "軸承摩擦係數 : ", "*查左表", 150, 20)
        self.bearing_pressured = self.AddLabeledTextCtrl(middel_sizer, "施予軸承負荷 : ", "N", 150, 20)
        self.bearing_outside_diameter = self.AddLabeledTextCtrl(middel_sizer, "外徑 :", "mm", 150, 20)
        self.bearing_inside_diameter = self.AddLabeledTextCtrl(middel_sizer, "內徑 : ", "mm", 150, 20)
        self.bearing_rpm = self.AddLabeledTextCtrl(middel_sizer, "軸承轉速 : ", "RPM", 150, 20)
        self.grease = self.AddLabeledTextCtrl(middel_sizer, "油脂黏度 : ", "mm²/s", 150, 20)
        self.bearing_count = self.AddLabeledTextCtrl(middel_sizer, "並列軸承數 : ", "個", 150, 20)
        self.temperature = self.AddLabeledTextCtrl(middel_sizer, "室溫 : ", "°C", 150, 20)
        text_sizer.Add(middel_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        # 右側下拉選擇欄位
        self.AddDropdown(text_sizer)
        # 加入欄位控制器
        input_sizer.Add(text_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizer.Add(input_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # 輸出欄位
        output_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="輸出區"), wx.HORIZONTAL)
        output_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        output_sizer.GetStaticBox().SetFont(output_font)
        output_sizer.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        output_sizer.GetStaticBox().SetMinSize(fixed_size)
        output_grid = wx.GridSizer(cols=3, vgap=20, hgap=20)
        # 輸出左側欄位
        output_left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.equivalent_bearing_load = self.AddLabeledTextCtrl(output_left_sizer, "軸承等效負荷 : ", "N", 220, 20, readonly=True)
        self.average_diameter = self.AddLabeledTextCtrl(output_left_sizer, "軸承平均徑 : ", "mm", 220, 20, readonly=True)
        self.bearing_torgue = self.AddLabeledTextCtrl(output_left_sizer, "軸承立矩估算 : ", "N-mm", 220, 20, readonly=True)
        self.bearing_heat = self.AddLabeledTextCtrl(output_left_sizer, "軸承輸出熱量預估 : ", "Kw", 220, 20, readonly=True)
        self.grease_coefficient = self.AddLabeledTextCtrl(output_left_sizer, "油脂入口剪切作用縮減係數 : ", "", 220, 20, readonly=True)
        # 輸出中間欄位
        output_middel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.total_torgue = self.AddLabeledTextCtrl(output_middel_sizer, "總力矩 : ", "N-mm", 150, 20, readonly=True)
        self.rotation_coefficient = self.AddLabeledTextCtrl(output_middel_sizer, "軸承滾動係數(Grr) : ", "", 150, 20, readonly=True)
        self.rotation_torgue = self.AddLabeledTextCtrl(output_middel_sizer, "軸承滾動力矩(Mrr) : ", "N-mm", 150, 20, readonly=True)
        self.sliding_coefficient = self.AddLabeledTextCtrl(output_middel_sizer, "軸承滑動係數(Gsl) : ", "", 150, 20, readonly=True)
        self.sliding_torgue = self.AddLabeledTextCtrl(output_middel_sizer, "軸承滑動力矩(Msl) : ", "N-mm", 150, 20, readonly=True)
        # 輸出右側欄位
        output_right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.signle_bearing_heat = self.AddLabeledTextCtrl(output_right_sizer, "單列軸承總輸出熱量 : ", "W", 150, 20, readonly=True)
        self.windcooling_temp = self.AddLabeledTextCtrl(output_right_sizer, "軸承溫度(風冷) : ", "°C", 150, 20, readonly=True)
        self.windcooling_tempterature_rise = self.AddLabeledTextCtrl(output_right_sizer, "溫升(風冷) : ", "°C", 150, 20, readonly=True)
        self.oilcooling_temp = self.AddLabeledTextCtrl(output_right_sizer, "軸承溫度(油冷) : ", "°C", 150, 20, readonly=True)
        self.oilcooling_tempterature_rise = self.AddLabeledTextCtrl(output_right_sizer, "溫升(油冷) : ", "°C", 150, 20, readonly=True)
        output_grid.Add(output_left_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        output_grid.Add(output_middel_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        output_grid.Add(output_right_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        output_sizer.Add(output_grid, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizer.Add(output_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)


        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)

        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.experssion)
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(20, 20)  # 設置滾動速率


    # 下拉選擇器
    def AddDropdown(self, sizer):
        # 創建下拉選擇欄位
        dropdown_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dropdown_lbl = wx.StaticText(self, label="選擇軸承滾珠類別 ： ", size=(200, 30))
        dropdown_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dropdown_lbl.SetFont(dropdown_font)
        dropdown_lbl.SetForegroundColour(wx.Colour(255,106,106))
        # 選項
        self.options = {"鋼珠":1, "陶珠":0.41}
        # 提取選項
        self.choices = list(self.options.keys())

        self.dropdown = wx.Choice(self, choices=self.choices, size=(80, 30))
        dropdown_sizer.Add(dropdown_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        dropdown_sizer.Add(self.dropdown, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(dropdown_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)


    def MergeImage(self, image_path, icon_path):
        # 加載背景圖片
        bg_image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        # 加載圖標圖片
        icon_image = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)
        # 重新調整圖標大小
        icon_image = icon_image.Scale(100, 150, wx.IMAGE_QUALITY_HIGH)
        icon_bmp = wx.Bitmap(icon_image)
        # 創建畫布
        bmp = wx.Bitmap(bg_image)
        width, height = bmp.GetSize()
        # 創建內存DC
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(bmp)
        # 繪制圖標到背景圖片
        icon_width, icon_height = icon_bmp.GetSize()
        icon_x = 10
        icon_y = height - icon_height
        mem_dc.DrawBitmap(icon_bmp, icon_x, icon_y, True)
        # 清理
        mem_dc.SelectObject(wx.NullBitmap)
        # 返回帶有圖標的背景圖片
        return bmp


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
        box.Add(lbl, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        box.Add(txt, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 添加到主布局
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)
        return txt


    def experssion(self,event):
        try :
            # 獲取選擇的選項
            selected_option = self.dropdown.GetStringSelection()
            # 根據選擇的選項獲取對應的係數
            bead_coefficient = self.options.get(selected_option)
            if bead_coefficient is None:
                raise ValueError("未選擇有效的選項")
            # 取值
            bearing_friction_coefficient = float(self.bearing_friction_coefficient.GetValue())
            bearing_pressured = float(self.bearing_pressured.GetValue())
            bearing_outside_diameter = float(self.bearing_outside_diameter.GetValue())
            bearing_inside_diameter = float(self.bearing_inside_diameter.GetValue())
            bearing_rpm = float(self.bearing_rpm.GetValue())
            grease = float(self.grease.GetValue())
            bearing_count = float(self.bearing_count.GetValue())
            temperature = float(self.temperature.GetValue())
            # 演算
            equivalent_bearing_load = bearing_pressured * 0.1
            average_diameter = (bearing_inside_diameter + bearing_outside_diameter)/2
            bearing_torgue = bearing_friction_coefficient * equivalent_bearing_load * bearing_inside_diameter * 0.5
            bearing_heat = 1.05 * 10**(-4) * bearing_torgue * bearing_rpm /1000
            grease_coefficient = 1 / (1 + (1.84 * 10 ** (1 / 9)) * ((bearing_rpm * average_diameter) ** 1.28) * (grease ** 0.64))
            rotation_coefficient = (5.03 * 10 ** (-12)) * (average_diameter ** 1.97) * (((equivalent_bearing_load * (1.9 * 10 ** (-12)) * bead_coefficient * (average_diameter ** 4) * (bearing_rpm ** 2)) + (1.97 * bearing_pressured)) ** 0.54)
            rotation_torgue = rotation_coefficient * (bearing_rpm * grease)**0.6
            relay_opertion = float((bead_coefficient * 1.91 * 10 ** (-12)) * (average_diameter ** 4) * (bearing_rpm ** 2)) # 中繼運算
            sliding_coefficient = (1.3 * 10 ** (-2)) * (average_diameter ** 0.26) * (((equivalent_bearing_load + relay_opertion) ** (4 / 3)) + (0.68 * (bearing_pressured ** (4 / 3))))
            sliding_torgue = sliding_coefficient *0.05
            total_torgue = (1 - (1 / (math.e ** (0.00000006 * grease * bearing_rpm * (bearing_outside_diameter + bearing_inside_diameter) * (4.4 / (2 * (bearing_outside_diameter - bearing_inside_diameter)) ** 0.5)))) * 0.05 + 0 * 0.15) * sliding_coefficient * grease_coefficient + sliding_torgue
            signle_bearing_heat = 1.05 * 10 ** (-4) * total_torgue * bearing_rpm
            windcooling_temp =  (temperature + (signle_bearing_heat / (1 * (bearing_outside_diameter ** 1.25) * ((0.0013 * 0.024) ** 0.33)))) * (1 + bearing_count * 0.147)
            windcooling_tempterature_rise = windcooling_temp - temperature
            oilcooling_temp = (temperature + (signle_bearing_heat / (1 * (bearing_outside_diameter ** 1.25) * ((0.88 * 1.97) ** 0.33)))) * (1 + bearing_count * 0.147)
            oilcooling_tempterature_rise = oilcooling_temp - temperature
            # 鋪陳
            self.equivalent_bearing_load.SetValue(f"{round(equivalent_bearing_load, 2)}")
            self.average_diameter.SetValue(f"{round(average_diameter, 2)}")
            self.bearing_torgue.SetValue(f"{round(bearing_torgue, 2)}")
            self.bearing_heat.SetValue(f"{round(bearing_heat, 6)}")
            self.grease_coefficient.SetValue(f"{round(grease_coefficient, 12)}")
            self.total_torgue.SetValue(f"{round(total_torgue, 2)}")
            self.rotation_coefficient.SetValue(f"{round(rotation_coefficient, 6)}")
            self.rotation_torgue.SetValue(f"{round(rotation_torgue, 6)}")
            self.sliding_coefficient.SetValue(f"{round(sliding_coefficient, 2)}")
            self.sliding_torgue.SetValue(f"{round(sliding_torgue, 2)}")
            self.signle_bearing_heat.SetValue(f"{round(signle_bearing_heat, 2)}")
            self.windcooling_temp.SetValue(f"{round(windcooling_temp, 2)}")
            self.windcooling_tempterature_rise.SetValue(f"{round(windcooling_tempterature_rise, 2)}")
            self.oilcooling_temp.SetValue(f"{round(oilcooling_temp, 2)}")
            self.oilcooling_tempterature_rise.SetValue(f"{round(oilcooling_tempterature_rise, 2)}")

        except ValueError as e:
            wx.MessageBox(f"輸入錯誤: {e}", "錯誤", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"計算錯誤: {e}", "錯誤", wx.OK | wx.ICON_ERROR)




# 斜角滾珠軸承壓力預估
class angular_bearing_pressure(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 畫面長寬設定
        fixed_size = wx.Size(1200,-1)
        # 畫面管理器
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # 載入GIF
        animation = wx.adv.Animation('images/navbar.gif')
        gif_ctrl = wx.adv.AnimationCtrl(self, -1, animation)
        # 設定GIF自動撥放
        gif_ctrl.Play()
        sizer.Add(gif_ctrl, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 軸承基本設定欄位
        base_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="基礎設定"), wx.HORIZONTAL)
        base_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        base_bg.GetStaticBox().SetFont(base_font)
        base_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        base_sizer = wx.GridSizer(cols=3, vgap=10, hgap=100)
        self.base_reload = self.AddLabeledTextCtrl(base_sizer, "基本預壓力(DF、DB) : ", "N", 200, 20, remark="※查原廠型錄")
        self.base_axial_rigidity = self.AddLabeledTextCtrl(base_sizer, "軸向剛性 : ", "N/µm", 80, 20, remark="※查原廠型錄")
        self.base_allowable_rpm = self.AddLabeledTextCtrl(base_sizer, "軸承容許轉速 : ", "RPM", 120, 20, remark="※查原廠型錄")
        base_bg.Add(base_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizer.Add(base_bg, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # 定位預壓與速度係數
        position_and_speed_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="定位預壓與速度係數"), wx.HORIZONTAL)
        position_and_speed_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        position_and_speed_bg.GetStaticBox().SetFont(position_and_speed_font)
        position_and_speed_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        position_and_speed_bg.GetStaticBox().SetMinSize(fixed_size)
        position_and_speed_sizer = wx.GridSizer(cols=2, vgap=20, hgap=150)
        # 圖片示意
        position_and_speed_image = wx.Image('images/Positioning_preload_and_speed_coefficient.png', wx.BITMAP_TYPE_PNG)
        position_and_speed_image = position_and_speed_image.Scale(461, 176, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(position_and_speed_image))
        position_and_speed_sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 欄位
        vertical_text = wx.BoxSizer(wx.VERTICAL)
        self.db_position_and_speed = self.AddLabeledTextCtrl(vertical_text, "定位預壓與速度係數(DB、DF) : ", "", 300, 20, remark="※查左表")
        self.dbd_position_and_speed = self.AddLabeledTextCtrl(vertical_text, "定位預壓與速度係數(DBD、DFD) : ", "", 300, 20, remark="※查左表")
        self.dbb_position_and_speed = self.AddLabeledTextCtrl(vertical_text, "定位預壓與速度係數(DBB、DFF) : ", "", 300, 20, remark="※查左表")
        self.dbbd_position_and_speed = self.AddLabeledTextCtrl(vertical_text, "定位預壓與速度係數(DBBD、DFFD) : ", "", 300, 20, remark="※查左表")
        position_and_speed_sizer.Add(vertical_text, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        position_and_speed_bg.Add(position_and_speed_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(position_and_speed_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 定位預壓係數
        preload_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="預壓係數"), wx.HORIZONTAL)
        preload_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        preload_bg.GetStaticBox().SetFont(preload_font)
        preload_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        preload_bg.GetStaticBox().SetMinSize(fixed_size)
        preload_sizer = wx.GridSizer(cols=2, vgap=20, hgap=150)
        # 圖片
        preload_image = wx.Image('images/preload_coefficient.jpg', wx.BITMAP_TYPE_JPEG)
        preload_image = preload_image.Scale(461, 164, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(preload_image))
        preload_sizer.Add(bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 欄位
        self.preload_coefficient = self.AddLabeledTextCtrl(preload_sizer, "預壓係數 : ", "", 80, 20, remark="※查左表")
        preload_bg.Add(preload_sizer, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(preload_bg, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # DB、DF輸出
        db_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="DB、DF組合"), wx.HORIZONTAL)
        db_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        db_bg.GetStaticBox().SetFont(db_font)
        db_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        db_bg.GetStaticBox().SetMinSize(fixed_size)
        db_sizer = wx.GridSizer(cols=2, vgap=20, hgap=300)
        self.db_radial_rigidity = self.AddLabeledTextCtrl(db_sizer, "徑向剛性 : ", "N/µm", 100, 20, readonly=True)
        self.db_allowable_rpm = self.AddLabeledTextCtrl(db_sizer, "容許轉速 : ", "RPM", 100, 20, readonly=True)
        db_bg.Add(db_sizer, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(db_bg, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # DBD、DFD輸出
        dbd_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="DBD、DFD組合"), wx.HORIZONTAL)
        dbd_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dbd_bg.GetStaticBox().SetFont(dbd_font)
        dbd_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        dbd_bg.GetStaticBox().SetMinSize(fixed_size)
        dbd_sizer = wx.GridSizer(cols=2, vgap=20, hgap=300)
        self.dbd_valid_preload = self.AddLabeledTextCtrl(dbd_sizer, "有效預壓力 : ", "N", 100, 20, readonly=True)
        self.dbd_allowable_rpm = self.AddLabeledTextCtrl(dbd_sizer, "容許轉速 : ", "RPM", 100, 20, readonly=True)
        self.dbd_radial_rigidity = self.AddLabeledTextCtrl(dbd_sizer, "徑向剛性 : ", "N/µm", 100, 20, readonly=True)
        self.dbd_axial_rigidity = self.AddLabeledTextCtrl(dbd_sizer, "軸向剛性 : ", "N/µm", 100, 20, readonly=True)

        dbd_bg.Add(dbd_sizer, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(dbd_bg, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # DBB、DFF輸出
        dbb_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="DBB、DFF組合"), wx.HORIZONTAL)
        dbb_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dbb_bg.GetStaticBox().SetFont(dbb_font)
        dbb_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        dbb_bg.GetStaticBox().SetMinSize(fixed_size)
        dbb_sizer = wx.GridSizer(cols=2, vgap=20, hgap=300)
        self.dbb_valid_preload = self.AddLabeledTextCtrl(dbb_sizer, "有效預壓力 : ", "N", 100, 20, readonly=True)
        self.dbb_allowable_rpm = self.AddLabeledTextCtrl(dbb_sizer, "容許轉速 : ", "RPM", 100, 20, readonly=True)
        self.dbb_radial_rigidity = self.AddLabeledTextCtrl(dbb_sizer, "徑向剛性 : ", "N/µm", 100, 20, readonly=True)
        self.dbb_axial_rigidity = self.AddLabeledTextCtrl(dbb_sizer, "軸向剛性 : ", "N/µm", 100, 20, readonly=True)

        dbb_bg.Add(dbb_sizer, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(dbb_bg, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # DBBD、DFFD輸出
        dbbd_bg = wx.StaticBoxSizer(wx.StaticBox(self, label="DBBD、DFFD組合"), wx.HORIZONTAL)
        dbbd_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dbbd_bg.GetStaticBox().SetFont(dbbd_font)
        dbbd_bg.GetStaticBox().SetForegroundColour(wx.Colour(255,106,106))
        dbbd_bg.GetStaticBox().SetMinSize(fixed_size)
        dbbd_sizer = wx.GridSizer(cols=2, vgap=20, hgap=300)
        self.dbbd_valid_preload = self.AddLabeledTextCtrl(dbbd_sizer, "有效預壓力 : ", "N", 100, 20, readonly=True)
        self.dbbd_allowable_rpm = self.AddLabeledTextCtrl(dbbd_sizer, "容許轉速 : ", "RPM", 100, 20, readonly=True)
        self.dbbd_radial_rigidity = self.AddLabeledTextCtrl(dbbd_sizer, "徑向剛性 : ", "N/µm", 100, 20, readonly=True)
        self.dbbd_axial_rigidity = self.AddLabeledTextCtrl(dbbd_sizer, "軸向剛性 : ", "N/µm", 100, 20, readonly=True)

        dbbd_bg.Add(dbbd_sizer, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(dbbd_bg, 0, wx.ALIGN_CENTER|wx.ALL, 10)


        # 設定按鈕圖案
        btn_icon = wx.Image("images/submit.png", wx.BITMAP_TYPE_PNG)
        btn_icon = btn_icon.Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        btn_bitmap = wx.Bitmap(btn_icon)

        # 添加計算按鈕
        calc_button = wx.BitmapButton(self, bitmap=btn_bitmap)
        calc_button.SetBackgroundColour(wx.Colour(255, 0, 0))
        calc_button.Bind(wx.EVT_BUTTON, self.experssion)
        sizer.Add(calc_button, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(20, 20)  # 設置滾動速率



    # 欄位新增器
    def AddLabeledTextCtrl(self, sizer, label, unit, label_width, label_high, readonly=False, remark=False):
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

        # 備註欄
        if remark :
            remark_grid = wx.BoxSizer(wx.VERTICAL)# 備註與欄位垂直
            lbl_box = wx.BoxSizer(wx.HORIZONTAL)  # 欄位水平排列
            lbl_box.Add(lbl, 0, wx.ALIGN_CENTER | wx.ALL, 0)
            lbl_box.Add(txt, 0, wx.ALIGN_CENTER | wx.ALL, 0)
            lbl_box.Add(unit_lbl, 0, wx.ALIGN_CENTER | wx.ALL, 0)
            remark_grid.Add(lbl_box, 0, wx.ALIGN_CENTER|wx.ALL, 0)

            remark_lbl = wx.StaticText(self, label=remark)
            remark_font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            remark_lbl.SetForegroundColour(wx.Colour(255,0,0))
            remark_lbl.SetFont(remark_font)
            remark_grid.Add(remark_lbl, 0, wx.ALIGN_CENTER|wx.LEFT, label_width)
            # 添加到主布局
            sizer.Add(remark_grid, 0, wx.EXPAND | wx.ALL, 10)

        else:
            box = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(lbl, 0, wx.ALIGN_CENTER | wx.ALL, 0)
            box.Add(txt, 0, wx.ALIGN_CENTER | wx.ALL, 0)
            box.Add(unit_lbl, 0, wx.ALIGN_CENTER | wx.ALL, 0)
            # 添加到主布局
            sizer.Add(box, 0, wx.EXPAND  | wx.ALL, 10)

        return txt

    def experssion(self, event):
        try:
            # 取值
            base_reload = float(self.base_reload.GetValue())
            base_axial_rigidity = float(self.base_axial_rigidity.GetValue())
            preload_coefficient = float(self.preload_coefficient.GetValue())
            base_allowable_rpm = float(self.base_allowable_rpm.GetValue())
            db_position_and_speed = self.db_position_and_speed.GetValue()
            dbd_position_and_speed = self.dbd_position_and_speed.GetValue()
            dbb_position_and_speed = self.dbb_position_and_speed.GetValue()
            dbbd_position_and_speed = self.dbbd_position_and_speed.GetValue()
            # 演算
            db_radial_rigidity = preload_coefficient * base_axial_rigidity
            db_allowable_rpm = base_allowable_rpm * float(db_position_and_speed)

            # 鋪陳
            self.db_radial_rigidity.SetValue(f"{round(db_radial_rigidity, 2)}")
            self.db_allowable_rpm.SetValue(f"{round(db_allowable_rpm, 2)}")

            if dbd_position_and_speed :
                # 運算
                dbd_valid_preload = 1.36 * base_reload
                dbd_allowable_rpm = base_allowable_rpm * float(dbd_position_and_speed)
                dbd_radial_rigidity = 1.54 *db_radial_rigidity
                dbd_axial_rigidity = 1.48 * base_axial_rigidity
                # 鋪陳
                self.dbd_valid_preload.SetValue(f"{round(dbd_valid_preload, 2)}")
                self.dbd_allowable_rpm.SetValue(f"{round(dbd_allowable_rpm, 2)}")
                self.dbd_radial_rigidity.SetValue(f"{round(dbd_radial_rigidity, 2)}")
                self.dbd_axial_rigidity.SetValue(f"{round(dbd_axial_rigidity, 2)}")
            else:
                # 如果dbd_position_and_speed是0，則清空相關欄位
                self.dbd_valid_preload.SetValue("")
                self.dbd_allowable_rpm.SetValue("")
                self.dbd_radial_rigidity.SetValue("")
                self.dbd_axial_rigidity.SetValue("")

            if dbb_position_and_speed :
                # 運算
                dbb_valid_preload = 2 * base_reload
                dbb_allowable_rpm = base_allowable_rpm * float(dbb_position_and_speed)
                dbb_radial_rigidity = 2 * db_radial_rigidity
                dbb_axial_rigidity = 2 * base_axial_rigidity
                # 鋪陳
                self.dbb_valid_preload.SetValue(f"{round(dbb_valid_preload, 2)}")
                self.dbb_allowable_rpm.SetValue(f"{round(dbb_allowable_rpm, 2)}")
                self.dbb_radial_rigidity.SetValue(f"{round(dbb_radial_rigidity, 2)}")
                self.dbb_axial_rigidity.SetValue(f"{round(dbb_axial_rigidity, 2)}")
            else:
                # 如果dbb_position_and_speed是0，則清空相關欄位
                self.dbb_valid_preload.SetValue("")
                self.dbb_allowable_rpm.SetValue("")
                self.dbb_radial_rigidity.SetValue("")
                self.dbb_axial_rigidity.SetValue("")

            if dbbd_position_and_speed :
                # 運算
                dbbd_valid_preload = 2.3 * base_reload
                dbbd_allowable_rpm = base_allowable_rpm * float(dbbd_position_and_speed)
                dbbd_radial_rigidity = 2.64 * db_radial_rigidity
                dbbd_axial_rigidity = 2.64 * base_axial_rigidity
                # 鋪陳
                self.dbbd_valid_preload.SetValue(f"{round(dbbd_valid_preload, 2)}")
                self.dbbd_allowable_rpm.SetValue(f"{round(dbbd_allowable_rpm, 2)}")
                self.dbbd_radial_rigidity.SetValue(f"{round(dbbd_radial_rigidity, 2)}")
                self.dbbd_axial_rigidity.SetValue(f"{round(dbbd_axial_rigidity, 2)}")
            else :
                # 如果dbbd_position_and_speed是0，則清空相關欄位
                self.dbbd_valid_preload.SetValue("")
                self.dbbd_allowable_rpm.SetValue("")
                self.dbbd_radial_rigidity.SetValue("")
                self.dbbd_axial_rigidity.SetValue("")

        except ValueError as e:
            wx.MessageBox(f"輸入錯誤: {e}", "錯誤", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"計算錯誤: {e}", "錯誤", wx.OK | wx.ICON_ERROR)




class ButtonRenderer(wx.grid.GridCellRenderer):
    def __init__(self, button_type, grid, callback):
        super().__init__()
        self.button_type = button_type
        self.grid = grid
        self.callback = callback

    def Draw(self, grid, attr, dc, rect, row, col, is_selected):
        # 設置繪圖顏色
        dc.SetTextForeground(wx.BLACK)
        # dc.SetBrush(wx.LIGHT_GREY_BRUSH)
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawRectangle(rect)

        # 繪製按鈕文本
        button_label = "刪除" if self.button_type == 'delete' else "修改"
        dc.DrawText(button_label, rect.x + 5, rect.y + 5)

    def GetBestSize(self, grid, attr, dc, row, col):
        return wx.Size(80, 30)  # 按鈕的大小

    def ActivateCell(self, grid, attr, row, col, mouse_event):
        if self.button_type == 'delete':
            wx.CallAfter(self.callback, row, 'delete')
        elif self.button_type == 'edit':
            wx.CallAfter(self.callback, row, 'edit')


class ButtonEditor(wx.grid.GridCellEditor):
    def __init__(self, button_type, callback, product_name, model_class):
        super().__init__()
        self.button_type = button_type
        self.callback = callback
        self.grid = None  # 這裡我們將在 Create 方法中設置
        self.product_name = product_name
        self.model_class = model_class

    def Create(self, parent, id, evt_handler):
        super().Create(parent, id, evt_handler)
        self.button = wx.Button(parent, id, label="刪除" if self.button_type == 'delete' else "修改")
        self.button.Bind(wx.EVT_BUTTON, self.OnClick)
        self.SetControl(self.button)

    def SetSize(self, rect):
        self.button.SetSize(rect)

    def OnClick(self, event):
        wx.CallAfter(self.callback, self.product_name, self.button_type, self.model_class)

    def EndEdit(self, row, col, grid):
        # 在這裡可以添加其他邏輯，例如更新單元格
        pass

    def BeginEdit(self, row, col, grid):
        self.grid = grid  # 在開始編輯時設置 grid

    def IsAcceptedKey(self, event):
        return False


# 搜尋視窗
class search_funtion(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        # 畫面長寬設定
        fixed_size = wx.Size(1200,-1)
        # 畫面管理器
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        # 載入GIF
        animation = wx.adv.Animation('images/you_right.gif')
        gif_ctrl = wx.adv.AnimationCtrl(self, -1, animation)
        # 設定GIF自動撥放
        gif_ctrl.Play()
        sizer.Add(gif_ctrl, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 搜尋介面
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.search_box = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(300,50))
        search_font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.search_box.SetFont(search_font)
        self.search_box.SetHint("搜尋")
        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.Judgmental)
        search_sizer.Add(self.search_box, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # 搜尋圖面
        image = wx.Image("images/magnifier.png", wx.BITMAP_TYPE_PNG)
        resized_image = image.Scale(48, 48, wx.IMAGE_QUALITY_HIGH)
        magnifier_bitmap = wx.Bitmap(resized_image)
        magnifier_button = wx.BitmapButton(self, bitmap=magnifier_bitmap)
        magnifier_button.Bind(wx.EVT_BUTTON, self.Judgmental)
        search_sizer.Add(magnifier_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        sizer.Add(search_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        # 欄位介面
        self.notebook = wx.Notebook(self)
        sizer.Add(self.notebook, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        # 添加不同的 Sheet
        self.add_sheet(self.notebook, session, SpindleMotor, "主軸馬達")
        self.add_sheet(self.notebook, session, ServoMotor, "伺服馬達")


        # 設置滾動區域
        self.SetScrollbars(50, 50, 50, 50)  # 設置捲動條，(水平步長, 垂直步長, 水平範圍, 垂直範圍)
        self.SetScrollRate(20, 20)  # 設置滾動速率


    def add_sheet(self, notebook, session, model_class, sheet_name):
        panel = wx.Panel(notebook)
        notebook.AddPage(panel, sheet_name)

        table_sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.grid.Grid(panel)

        records = session.query(model_class).all()
        chi_headers, columns = self.get_model_name(model_class)

        data = []
        for record in records:
            row = []
            for column in columns:
                value = getattr(record, column)
                if column == 'manufacturer_id':
                    manufacturer = session.query(Manufacturer).filter_by(id=value).first()
                    value = manufacturer.manufacturer_name if manufacturer else '未知'
                row.append(value)
            data.append(row)

        grid.CreateGrid(len(data), len(chi_headers)+2)

        # 欄位名稱
        for col, column_name in enumerate(chi_headers):
            grid.SetColLabelValue(col, column_name)
        grid.SetColLabelValue(len(chi_headers), "刪除")
        grid.SetColLabelValue(len(chi_headers)+1, "修改")

        # 資料鋪陳
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                grid.SetCellValue(row_index, col_index, str(cell_data))

            # 添加刪除和修改按鈕
            grid.SetCellRenderer(row_index, len(chi_headers), ButtonRenderer('delete', grid, self.on_button_click))
            grid.SetCellRenderer(row_index, len(chi_headers) + 1, ButtonRenderer('edit', grid, self.on_button_click))
            grid.SetCellEditor(row_index, len(chi_headers), ButtonEditor('delete', self.on_button_click, row_data[0], model_class))
            grid.SetCellEditor(row_index, len(chi_headers) + 1, ButtonEditor('edit', self.on_button_click, row_data[0], model_class ))


        grid.Fit()
        table_sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(table_sizer)


    def on_button_click(self, product_name, button_type, model_class):
        if button_type == 'delete':
            self.click_delete(product_name, model_class)
        elif button_type == 'edit':
            self.click_edit(product_name, model_class)


    def click_delete(self, product_name, model_class):
        # 刪除行的操作
        print(f"刪除行 {product_name}")
        print(f"資料庫名稱{model_class}")
        # 在這裡添加實際的刪除邏輯
        if model_class == ServoMotor:
            dialog = DeleteDialog(self, "刪除資料", product_name, model_class, refresh_callback=self.refresh_servo)
        else:
            dialog = DeleteDialog(self, "刪除資料", product_name, model_class, refresh_callback=self.refresh_spindle)
        dialog.ShowModal()
        dialog.Destroy()


    def click_edit(self, product_name, model_class):
        # 編輯行的操作
        print(f"編輯行 {product_name}")
        print(f"資料庫名稱{model_class}")
        # 在這裡添加實際的編輯邏輯
        if model_class == ServoMotor:
            dialog = ModifyDialog(self, "修改資料", product_name, model_class, refresh_callback=self.refresh_servo)
        else:
            dialog = ModifyDialog(self, "修改資料", product_name, model_class, refresh_callback=self.refresh_spindle)
        dialog.ShowModal()
        dialog.Destroy()


    def get_model_name(self,model):
        # 抓取中文名稱
        chi_headers = []
        columns = []
        for column in model.__table__.columns.values():
            if not column.primary_key:  # 排除主键列
                # 從 info 中的 'chinese_name'
                if column.info.get('unit'):
                    unit = column.info.get('unit')
                    chinese_name = f"{column.info.get('chinese_name')}" + f"({unit})"
                else:
                    chinese_name = f"{column.info.get('chinese_name')}"
                chi_headers.append(chinese_name)
                columns.append(column.name)
        return chi_headers, columns


    def Judgmental(self, event):
        text = self.search_box.GetValue()
        if text == "Insert_servo":
            self.show_insert_servo()
        elif text == "Insert_spindle":
            self.show_insert_spindle()


    def show_insert_servo(self):
        dialog = InsertDialog(self, "新增資料", ServoMotor, refresh_callback=self.refresh_servo)
        dialog.ShowModal()
        dialog.Destroy()


    def show_insert_spindle(self):
        dialog = InsertDialog(self, "新增資料", SpindleMotor, refresh_callback=self.refresh_spindle)
        dialog.ShowModal()
        dialog.Destroy()


    # 刷新伺服馬達頁面
    def refresh_servo(self):
        for page_index in range(self.notebook.GetPageCount()):
            if self.notebook.GetPageText(page_index) == "伺服馬達":
                self.notebook.RemovePage(page_index)
                self.add_sheet(self.notebook, session, ServoMotor, "伺服馬達")
                break


    # 刷新主軸馬達頁面
    def refresh_spindle(self):
        for page_index in range(self.notebook.GetPageCount()):
            if self.notebook.GetPageText(page_index) == "主軸馬達":
                self.notebook.RemovePage(page_index)
                self.add_sheet(self.notebook, session, SpindleMotor, "主軸馬達")
                break


