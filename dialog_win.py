import wx
from model import *
from collections import OrderedDict

class ManufacturerNotFoundError(Exception):
    pass

class DataComparisonError(Exception):
    pass

# 新增機制小視窗
class InsertDialog(wx.Dialog):
    def __init__(self, parent, title, model, refresh_callback=None):
        super().__init__(parent, title=title)
        self.model = model
        self.session = session
        self.fields = {}
        self.init_ui()
        self.refresh_callback = refresh_callback

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

    def on_save(self, event):
        # 將數據插入資料庫
        try:
            data = self.get_data() # 取得使用者輸入的資料
            self.insert_data(data)
            wx.MessageBox('資料已成功儲存!', '訊息', wx.OK | wx.ICON_INFORMATION)
            if self.refresh_callback:
                self.refresh_callback()  # 通知刷新
            self.EndModal(wx.ID_OK)  # 結束並關閉
        except Exception as e:
            wx.MessageBox(f'資料儲存失敗: {e}', '錯誤', wx.OK | wx.ICON_ERROR)
        except ManufacturerNotFoundError as e:
            wx.MessageBox(f'{e}', '錯誤', wx.OK | wx.ICON_ERROR)

    def save_countinue(self, event):
        # 將數據插入資料庫
        try:
            data = self.get_data() # 取得使用者輸入的資料# 取得使用者輸入的資料
            self.insert_data(data)
            wx.MessageBox('資料已成功儲存!', '訊息', wx.OK | wx.ICON_INFORMATION)
            if self.refresh_callback:
                self.refresh_callback()  # 通知刷新
            self.clear_fields()  # 清空輸入框，準備下一筆資料輸入
        except ManufacturerNotFoundError as e:
            wx.MessageBox(f'{e}', '錯誤', wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f'資料儲存失敗: {e}', '錯誤', wx.OK | wx.ICON_ERROR)


    def get_data(self):
        data = {}
        for field_name, text_ctrl in self.fields.items():
            value = text_ctrl.GetValue()
            if field_name == 'manufacturer_id':  # 假設你有一個叫做 'manufacturer_name' 的欄位
                # 查找廠商 ID
                manufacturer = self.session.query(Manufacturer).filter_by(manufacturer_name=value).first()
                if manufacturer:
                    data['manufacturer_id'] = manufacturer.id
                else:
                    raise ManufacturerNotFoundError(f"找不到 '{value}' 廠商")
            else:
                data[field_name] = value
        return data

    # 建立資料
    def insert_data(self, data):
        new_record = self.model(**data)
        self.session.add(new_record)
        self.session.commit()

    # 清空所有輸入框中的資料
    def clear_fields(self):
        for text_ctrl in self.fields.values():
            text_ctrl.SetValue("")


# 刪除機制小視窗
class DeleteDialog(wx.Dialog):
    def __init__(self, parent, title, product_name, model, refresh_callback=None):
        super().__init__(parent, title=title)
        self.product_name = product_name
        self.model = model
        self.session = session
        self.refresh_callback = refresh_callback
        self.field = None
        self.init_ui()
        print(self.product_name, self.model)

    def init_ui(self):
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(dialog_sizer)

        # 圖片
        delete_image = wx.Image('images/you_sure.jpg', wx.BITMAP_TYPE_JPEG)
        delete_image = delete_image.Scale(600, 393, wx.IMAGE_QUALITY_HIGH)
        delete_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(delete_image))
        dialog_sizer.Add(delete_bitmap, 0, wx.ALL | wx.CENTER, 10)

        # 提示用戶確定删除
        message = f"確定要刪除  「{self.product_name}」  嗎？"
        msg_text = wx.StaticText(self, label=message, style=wx.ALIGN_CENTER)
        text_font = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        msg_text.SetFont(text_font)
        msg_text.SetForegroundColour(wx.Colour(255,0,0))
        dialog_sizer.Add(msg_text, 0, wx.CENTER | wx.ALL, 30)

        # 自定義按鈕
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        delete_button = wx.Button(self, wx.ID_OK, label="刪除")
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete)
        cancel_button = wx.Button(self, wx.ID_CANCEL, label="取消")
        # 添加按鈕到佈局中
        btn_sizer.Add(delete_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        dialog_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)

        # 自動調整視窗大小及位置至中
        self.Fit()
        self.Center()


    def on_delete(self, event):
        # 將數據刪除
        try:
            record = self.session.query(self.model).filter_by(name=self.product_name).first()
            print(record)
            if record:
                self.session.delete(record)
                self.session.commit()
                wx.MessageBox('資料已成功刪除!', '訊息', wx.OK | wx.ICON_INFORMATION)
                if self.refresh_callback:
                    self.refresh_callback()  # 通知刷新
                self.EndModal(wx.ID_OK)  # 結束並關閉
            else:
                wx.MessageBox('找不到該記錄!', '錯誤', wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f'刪除失敗: {e}', '錯誤', wx.OK | wx.ICON_ERROR)



# 修改機制小視窗
class ModifyDialog(wx.Dialog):
    def __init__(self, parent, title, product_name, model, refresh_callback=None):
        super().__init__(parent, title=title)
        self.model = model
        self.session = session
        self.refresh_callback = refresh_callback
        self.product_name = product_name
        self.fields = {}
        self.init_ui()

    def init_ui(self):
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(dialog_sizer)

        # 根據模型動態生成輸入欄位
        for col in self.model.__table__.columns:
            chinese_name = col.info.get('chinese_name')
            unit = col.info.get('unit')
            if chinese_name or unit :
                self.AddLabeledTextCtrl(dialog_sizer, f"{chinese_name} : ", f"{unit}", 150, 20, col.name)
        # 抓取資料
        motified_data = session.query(self.model).filter_by(name=self.product_name).first()
        # 資料排列
        ordered_data = OrderedDict()
        ordered_data['name'] = motified_data.name
        ordered_data['rate_output'] = motified_data.rate_output
        ordered_data['torgue'] = motified_data.torgue
        ordered_data['speed'] = motified_data.speed
        ordered_data['max_torgue'] = motified_data.max_torgue
        ordered_data['max_speed'] = motified_data.max_speed
        ordered_data['weight'] = motified_data.weight
        manufacturer = session.query(Manufacturer).filter_by(id=motified_data.manufacturer_id).first() # 抓取製造商名稱
        ordered_data['manufacturer_id'] = manufacturer.manufacturer_name

        # 鋪陳資料到 TextCtrl
        self.set_data_to_fields(ordered_data)

        # 自定義按鈕
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        modify_button = wx.Button(self, wx.ID_OK, label="修改")
        modify_button.Bind(wx.EVT_BUTTON, self.on_modify)
        cancel_button = wx.Button(self, wx.ID_CANCEL, label="取消")
        # 添加按鈕到佈局中
        btn_sizer.Add(modify_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        dialog_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)
        # 自動調整視窗大小及位置至中
        self.Fit()
        self.Center()

    def AddLabeledTextCtrl(self, sizer, label, unit, width, high, field_name):
        box = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=label, size=(width, high))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl.SetFont(font)
        txt = wx.TextCtrl(self, size=(100, 20))
        self.fields[field_name] = txt  # 儲存所有欄位
        unit_lbl = wx.StaticText(self, label=unit)
        # 加入畫面
        box.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(unit_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 5)

    # 將資料鋪陳至textctrl
    def set_data_to_fields(self, ordered_data):
         for field_name, value in ordered_data.items():
            if field_name in self.fields:
                self.fields[field_name].SetValue(str(value))


    def on_modify(self, event):
        try:
            data = self.get_data()  # 取得使用者輸入的資料
            record_id = data.pop('name')
            record = self.session.query(self.model).filter_by(name=record_id).first()
            print(record)
            if record:
                for key, value in data.items():
                    setattr(record, key, value)
                self.session.commit()
                wx.MessageBox('資料已成功修改!', '訊息', wx.OK | wx.ICON_INFORMATION)
                if self.refresh_callback:
                    self.refresh_callback()  # 通知刷新
                self.EndModal(wx.ID_OK)  # 結束並關閉
            else:
                wx.MessageBox('找不到該記錄!', '錯誤', wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f'修改失敗: {e}', '錯誤', wx.OK | wx.ICON_ERROR)

    def get_data(self):
        data = {}
        for field_name, text_ctrl in self.fields.items():
            value = text_ctrl.GetValue()
            data[field_name] = value
        # 廠商比對
        if field_name == 'manufacturer_id':
            # 查找廠商 ID
            manufacturer = self.session.query(Manufacturer).filter_by(manufacturer_name=value).first()
            if manufacturer:
                data['manufacturer_id'] = manufacturer.id
            else:
                raise ManufacturerNotFoundError(f"找不到 '{value}' 廠商")
        print(data)
        return data
