import pandas as pd
from pathlib import Path

filepath = 'test1.csv'
print(Path(filepath))
#print(Path(filepath).read_text())
#aa=Path(filepath).read_text()
#print(aa[0])
#bb=pd.read_csv(filepath,encoding="sjis")
bb=pd.read_csv(filepath)
print (bb)
print(type(bb))
#for item in aa:
#   print(item)