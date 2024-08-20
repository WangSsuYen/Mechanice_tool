import pandas as pd
import sys

class read_excel:
    def __init__(self) -> None:
        self.file_path = 'tool/reduction_coefficient.xlsx'

    def belt_selection(self, RPM, Kw):
        datas = pd.read_excel(self.file_path, sheet_name="belt_selection")
        cols = datas.columns.ravel()
        for col in cols[1:] :
            if Kw <= int(col) :
                self.RPM = datas.set_index('皮帶輪迴轉速度(PRM)')[col].to_dict()
                for rpm in self.RPM :
                    if RPM >= rpm :
                        return self.RPM[rpm]


    def Kθ_value(self, value):
        datas = pd.read_excel(self.file_path, sheet_name="Kθ")
        self.Kθ_datas = datas.set_index('小皮帶輪接觸角度')['補正係數'].to_dict()
        for i in self.Kθ_datas:
            if  value >= i:
                return self.Kθ_datas[i]


    def Kl_value(self, value, type):
        datas = pd.read_excel(self.file_path,sheet_name="Kl",)
        self.Kl_datas = datas.set_index("皮帶周長")[type].to_dict()
        for i in self.Kl_datas:
            if value <= i :
                return self.Kl_datas[i]

    def ps_value(self):
        pass


    def pa_value(self):
        pass




# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python data.py <value>")
#         sys.exit(1)

#     value = float(sys.argv[1])
#     reader = read_excel()
#     reader.Kl_value(value)