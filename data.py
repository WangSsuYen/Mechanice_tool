import pandas as pd
import sys

class read_excel:
    def __init__(self) -> None:
        self.file_path = 'tool/reduction_coefficient.xlsx'

    def Kθ_value(self, value):
        datas = pd.read_excel(self.file_path, sheet_name="Kθ")
        self.Kθ_datas = datas.set_index('小皮帶輪接觸角度')['補正係數'].to_dict()
        for i in self.Kθ_datas:
            if  value >= i:
                return self.Kθ_datas[i]

