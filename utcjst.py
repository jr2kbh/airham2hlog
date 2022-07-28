from datetime import datetime
from dateutil import tz
import sys
import re
JST = tz.gettz('Asia/Tokyo')
UTC = tz.gettz("UTC")
ts = datetime.strptime(
                '2022-07-11 06:28:00 UTC',
                '%Y-%m-%d %H:%M:%S %Z')  # '2020-12-12 16
ts=ts.replace(tzinfo=UTC)
print(ts.isoformat())
t1=ts.astimezone(JST)
print(t1.isoformat())
t2=ts.astimezone(UTC)
print(t2.isoformat())
va='%Y-%m-%d %H:%M:%S %z'
ts = datetime.strptime(
                '2022-07-11 15:28:00 +09:00',
                va)  # '2020-12-12 16
print('1=',ts.isoformat())
t1=ts.astimezone(JST)
print(t1.isoformat())
t2=ts.astimezone(UTC)
print(t2.isoformat())

td=datetime.today().date().strftime('%Y-%m-%d')
tx=datetime.strptime(td,"%Y-%m-%d")
print(tx)
tdd=datetime.now()
if tdd>tx:
   
     print ("jj")
print (tdd,tx)
str='JCC0903: 上田 - Ueda (長野)'
m=re.search(r'(\d+): (.+) -.*\((.+)\)', str) 
print (m)
print(m.group(1),'--',m.group(2),'--',m.group(3))
qth=m.group(2)+'/'+m.group(3)
print (qth)