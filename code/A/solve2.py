'''
@Author: Hata
@Date: 2020-06-02 18:30:23
@LastEditors: Hata
@LastEditTime: 2020-06-04 08:45:08
@FilePath: \MCM2020\code\A\solve2.py
@Description: 
'''
import matplotlib.pyplot as plt
import numpy as np

from data import Data
from tree import MST

figure, ax = plt.subplots()
data = Data('.\\code\\A\\data.csv')
mst = MST(data.Translate('V|P'))
tr = mst.translator
mst.Build(0)
lines = mst.lines
deleteList = []
for i in range(len(lines)):
    begin = tr(lines[i][0])
    end = tr(lines[i][1])
    if('V' in begin[1] or 'V' in end[1]):
        deleteList.append(i)
mst.lines = np.delete(mst.lines, deleteList, axis=0)
mst.Draw(ax)
x = lines[:, -1].sum()
mst = MST(data.Translate('A|V'))
lines = mst.Build(0)
y = lines[:, -1].sum()
mst.Draw(ax)
data.Draw(ax)
print(x+y)
plt.show()
