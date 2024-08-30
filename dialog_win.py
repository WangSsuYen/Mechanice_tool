import wx
from model import *

# 新增機制小視窗
class InsertDialog(wx.Dialog):
    def __init__(self, parent, title, model):
        super().__init__(parent, title=title)
        self.model = model
        self.session = session
        self.fields = {}
        self.init_ui()

    def init_ui(self):
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(dialog_sizer)
        # 根據模型動態生成輸入欄位
        # labels = self.get_table_label(self.model)
        for col in self.model.__table__.columns:
            chinese_name = col.info.get('chinese_name')
            unit = col.info.get('unit')
            if chinese_name or unit :
                self.AddLabeledTextCtrl(dialog_sizer, f"{chinese_name} : ", f"{unit}", 150, 20, col.name)
        # 自定義按鈕
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(self, wx.ID_OK, label="儲存")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        save_continue_button = wx.Button(self, label="儲存並繼續下一筆")
        save_continue_button.Bind(wx.EVT_BUTTON, self.save_countinue)
        cancel_button = wx.Button(self, wx.ID_CANCEL, label="取消")
        # 添加按鈕到佈局中
        btn_sizer.Add(save_button, 0, wx.ALL, 5)
        btn_sizer.Add(save_continue_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        dialog_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)
        # 自動調整視窗大小及位置致中
        self.Fit()
        self.Center()


    def AddLabeledTextCtrl(self, sizer, label, unit, width, high, field_name):
        box = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=label, size=(width, high))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl.SetFont(font)
        txt = wx.TextCtrl(self, size=(100, 20))
        self.fields[field_name] = txt # 將輸入值與field_name串接關係。儲存資料為{fields["name"]:名稱}
        unit_lbl = wx.StaticText(self, label=unit)
        # 加入畫面
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

    # 儲存
    def on_save(self, event):
        # 取得使用者輸入的資料
        data = {}
        for field_name, text_ctrl in self.fields.items():
            data[field_name] = text_ctrl.GetValue()

        # 嘗試將數據插入資料庫
        try:
            self.insert_data(data)
            wx.MessageBox('資料已成功儲存!', '訊息', wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK) # 結束並關閉
        except Exception as e:
            wx.MessageBox(f'資料儲存失敗: {e}', '錯誤', wx.OK | wx.ICON_ERROR)

    # 儲存後繼續下一筆輸入
    def save_countinue(self, event):
        # 取得使用者輸入的資料
        data = {}
        for field_name, text_ctrl in self.fields.items():
            data[field_name] = text_ctrl.GetValue()
        # 嘗試將數據插入資料庫
        try:
            self.insert_data(data)
            wx.MessageBox('資料已成功儲存!', '訊息', wx.OK | wx.ICON_INFORMATION)
            self.clear_fields()  # 清空輸入框，準備下一筆資料輸入
        except Exception as e:
            wx.MessageBox(f'資料儲存失敗: {e}', '錯誤', wx.OK | wx.ICON_ERROR)

    # 建立資料
    def insert_data(self, data):
        new_record = self.model(**data)
        self.session.add(new_record)
        self.session.commit()

    # 清空所有輸入框中的資料
    def clear_fields(self):
        for text_ctrl in self.fields.values():
            text_ctrl.SetValue("")


