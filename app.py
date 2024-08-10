import wx

class MechanicsCalculator(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='力學計算機')
        panel = wx.Panel(self)

        # Create main sizer
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left side - buttons
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons = ['力學計算機', '螺桿推力', '皮帶', '流體力學']
        for label in buttons:
            button = wx.Button(panel, label=label)
            button_sizer.Add(button, 0, wx.ALL, 5)

        # Right side - content
        content_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="示範圖片")
        content_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Image placeholder
        image_placeholder = wx.StaticText(panel, label="[圖片顯示區域]", style=wx.ALIGN_CENTER)
        image_placeholder.SetMinSize((300, 200))
        content_sizer.Add(image_placeholder, 0, wx.ALL | wx.EXPAND, 5)

        # Input fields
        grid_sizer = wx.FlexGridSizer(5, 4, 10, 10)

        labels = [
            "馬達力矩:", "螺桿直徑:",
            "螺桿導程:", "導程角:",
            "損失估算:", "",
            "流量:", "面積:",
            "壓力:", "溫度:"
        ]
        units = ["N.M", "mm", "mm", "Deg", "%", "", "m3/hr", "m2", "Kg/cm2", "°C"]

        for label, unit in zip(labels, units):
            if label:
                grid_sizer.Add(wx.StaticText(panel, label=label))
                text_ctrl = wx.TextCtrl(panel)
                grid_sizer.Add(text_ctrl)
                grid_sizer.Add(wx.StaticText(panel, label=unit))
                grid_sizer.AddSpacer(1)
            else:
                grid_sizer.AddSpacer(1)
                grid_sizer.AddSpacer(1)
                grid_sizer.AddSpacer(1)
                grid_sizer.AddSpacer(1)

        content_sizer.Add(grid_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Calculate button
        calc_button = wx.Button(panel, label="送出計算")
        content_sizer.Add(calc_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Add sizers to main sizer
        main_sizer.Add(button_sizer, 0, wx.ALL, 10)
        main_sizer.Add(content_sizer, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(main_sizer)
        self.SetSize((600, 400))
        self.Centre()

if __name__ == '__main__':
    app = wx.App()
    frame = MechanicsCalculator()
    frame.Show()
    app.MainLoop()