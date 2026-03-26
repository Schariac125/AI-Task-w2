import pandas as pd

data = pd.read_csv("information.csv",na_values=['无附件','-1','-1'])
a = data.head()
b = a.loc[a.文件下载次数.isnull()]
print(b)
