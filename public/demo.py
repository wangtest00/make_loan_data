import sys
import os
import io
import datetime
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
import matplotlib.pyplot as plt
from pandas.plotting import table
import pandas as pd

fig = plt.figure(figsize=(9,10),dpi=140)
ax = fig.add_subplot(111, frame_on=False,)
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis
datas = pd.read_excel('C:\\Users\\wangshuang\\Desktop\\更换产品.xls')
print(datas)
datas = datas.iloc[:,0:]
print(datas)
table(ax, datas, loc='center')  # where df is your data frame
plt.savefig('./photo.jpg')