import wx


class Frame(wx.Frame):

    def __init__(self, *args, **kw):
        super().__init__(parent=None, title='Yang Iron Mechanice Tools')


    # 側邊選單
    def side_menu():
        pass


    # 主介面
    def main_control_panel():
        pass



if __name__ == '__main__':
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()