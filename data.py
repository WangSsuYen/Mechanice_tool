import pandas as pd
import sys

class read_excel:
    def __init__(self) -> None:
        self.file_path = 'tool/reduction_coefficient.xlsx'

    def belt_selection(self, RPM, Kw):
        datas = pd.read_excel(self.file_path, sheet_name="belt_selection")
        cols = datas.columns.ravel()
        last_col = cols[1]
        for col in cols[1:] :
            if Kw <= int(col) :
                self.RPM = datas.set_index('皮帶輪迴轉速度(PRM)')[last_col].to_dict()
                for rpm in self.RPM :
                    if RPM >= rpm :
                        print(self.RPM[rpm])
                        return self.RPM[rpm]
            last_col = col


    def Kθ_value(self, value):
        datas = pd.read_excel(self.file_path, sheet_name="Kθ")
        self.Kθ_datas = datas.set_index('小皮帶輪接觸角度')['補正係數'].to_dict()
        for i in self.Kθ_datas:
            if  value >= i:
                print(self.Kθ_datas[i])
                return self.Kθ_datas[i]


    def Kl_value(self, value, type):
        datas = pd.read_excel(self.file_path,sheet_name="Kl",)
        self.Kl_datas = datas.set_index("皮帶中心距")[type].to_dict()
        for i in self.Kl_datas:
            if value <= i :
                print(self.Kl_datas[i])
                return self.Kl_datas[i]


    def ps_value(self, belt_selection, spindle_RPM, spindle_pulley_diameter):
        datas = pd.read_excel(self.file_path, sheet_name=f"{belt_selection}_motion_coefficient")
        cols = datas.columns.ravel()
        last_col = cols[1]
        fina_col = cols[-1]
        for col in cols[1:]:
            if float(spindle_pulley_diameter) < float(col) :
                self.ps_datas = datas.set_index("皮帶輪迴轉速度(PRM)")[last_col].to_dict()
                for rpm in self.ps_datas:
                    if float(spindle_RPM) <= float(rpm):
                        print(self.ps_datas[rpm])
                        return float(self.ps_datas[rpm])

            elif float(spindle_pulley_diameter) >= float(fina_col):
                self.ps_datas = datas.set_index("皮帶輪迴轉速度(PRM)")[fina_col].to_dict()
                for rpm in self.ps_datas:
                    if float(spindle_RPM) <= float(rpm):
                        print(self.ps_datas[rpm])
                        return float(self.ps_datas[rpm])

            last_col = col


    def pa_value(self, belt_selection, spindle_RPM, motor_RPM):
        datas = pd.read_excel(self.file_path, sheet_name=f"{belt_selection}_rotation_coefficient")
        cols = datas.columns.ravel()
        last_col = cols[1]
        fina_col = cols[-1]
        for col in cols[1:]:
            if float(motor_RPM)/float(spindle_RPM) < float(col):
                self.pa_datas = datas.set_index("皮帶輪迴轉速度(PRM)")[last_col].to_dict()
                for rpm in self.pa_datas:
                    if float(spindle_RPM) <= float(rpm):
                        print(self.pa_datas[rpm])
                        return float(self.pa_datas[rpm])

            elif float(motor_RPM)/float(spindle_RPM) >= float(fina_col):
                self.pa_datas = datas.set_index("皮帶輪迴轉速度(PRM)")[fina_col].to_dict()
                for rpm in self.pa_datas:
                    if float(spindle_RPM) <= float(rpm):
                        print(self.pa_datas[rpm])
                        return float(self.pa_datas[rpm])
            last_col = col




# if __name__ == "__main__":
#     belt_selection = sys.argv[1]
#     spindle_RPM = sys.argv[2]
#     motor_RPM = sys.argv[3]
#     reader = read_excel()
#     reader.pa_value(belt_selection, spindle_RPM, motor_RPM)