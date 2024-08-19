import pandas as pd

class read_excel:
    def __init__(self) -> None:
        data = pd.read_excel('tool/reduction_coefficient.xlsx', sheet_name=None)



        for sheet_name, df in data.items():
            print(f"Sheet: {sheet_name}")
            print(df)  # 打印前5行內容